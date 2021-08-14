__author__ = "Andrew Gree"
__copyright__ = "CriticalHop Inc."
__license__ = "MIT"


from contextlib import contextmanager
import sys
import tempfile
import types
import hyperc

_file_cache = {}
_dirty_is_context = False 

def _get_indent(l):
    return len(l) - len(l.lstrip())

def _stub_rewrite_while_choice(code, frame):
    """A stub to rewrite while ... choice to assert ...
    
    Currently `while ..` loop only serves as a "mental model" around HyperC
    """
    for ln in range(len(code)):
        print(code[ln], code[ln+1])
        l = code[ln]
        if (l.strip().startswith("while") and 
            (
                code[ln+1].strip().startswith("ordered.choice") or
                code[ln+1].strip().startswith("random.choice") or
                code[ln+1].strip().startswith("choice")
             )):
             # TODO: strip out comments!
            if "#" in code[ln]: raise ValueError("Comments not supported on while... line") 
            code[ln] = l.replace("while", "assert not (").replace(":", "") + ")"
            choiceline = code[ln+1]
            choice_indent = _get_indent(choiceline)
            code[ln+1] = "#"+code[ln+1]
            if len(code) > ln+2 and code[ln+2].strip() and _get_indent(code[ln+2]) == choice_indent:
                raise ValueError(f"Unsupported while...choice loop complexity: extra `{code[ln+2].strip()}`")
            break
    else:
        raise ValueError("while...ordered.choice() was not found in ordered context block")
    
    choiceargs = []
    def choice(*args):
        def consume(*args):
            choiceargs.append(args)
        choiceargs.append(args)
        return consume
    class OrderedStub:
        pass
    ordered = OrderedStub()
    ordered.choice = choice
    def get_objects():
        return "GC_OBJECTS"
    gc = OrderedStub()
    gc.get_objects = get_objects
    stub_globals = frame.f_globals.copy()
    stub_locals = frame.f_locals.copy()
    stub_globals["choice"] = choice
    stub_globals["choices"] = choice
    stub_globals["ordered"] = ordered
    stub_globals["random"] = ordered
    stub_globals["gc"] = gc 
    stub_locals["choice"] = choice
    stub_locals["choices"] = choice
    stub_locals["ordered"] = ordered
    stub_locals["random"] = ordered
    stub_locals["gc"] = gc 
    eval(choiceline, stub_globals, stub_locals)

    # TODO: support situation when choosing with no arguments - from funcitons defined in local context
    # the code within the orderedcontext block may include functions to compile
    # these functions must be compiled using "normal" flow of program

    if len(choiceargs) < 2 or len(choiceargs) > 3:
        raise ValueError("Unsupported ordered.choice invocation")
    choiceargs_parsed = {}
    if choiceargs[0] and choiceargs[1]:
        choiceargs_parsed['functions'] = {
            f.__name__:f for f in filter(
                lambda x: 
                isinstance(x, types.FunctionType) or isinstance(x, type), 
                choiceargs[0][0])}
        choiceargs_parsed['objects'] = choiceargs[1][0]
    elif choiceargs[0] and not choiceargs[1]:
        choiceargs_parsed['functions'] = {
            f.__name__:f for f in filter(
                lambda x: 
                isinstance(x, types.FunctionType) or isinstance(x, type), 
                choiceargs[0][0])}
        choiceargs_parsed['objects'] = "GC_OBJECTS"
    elif not choiceargs[0] and choiceargs[1]:
        choiceargs_parsed['functions'] = frame.f_locals  # FIXME: use collected by trace
        choiceargs_parsed['objects'] = choiceargs[1][0]
    elif not choiceargs[0] and not choiceargs[1]:
        choiceargs_parsed['functions'] = frame.f_locals  # FIXME: use collected by trace
        choiceargs_parsed['objects'] = "GC_OBJECTS"
    else: 
        raise ValueError("Unsupported choice configuration")

    #print("Choice args parsed:", choiceargs_parsed)
    #print("Choice args:", choiceargs)

    return code, choiceargs_parsed


def _cached_code(fn):
    code = _file_cache.get(fn)
    if not code:
        code = open(fn).read().split("\n")
        _file_cache[fn] = code
    return code

def _scan_to_exitcontext(frame):
    "Return code_of_context, exit_lineno"
    lineno = frame.f_lineno-1
    cur_line = _cached_code(frame.f_code.co_filename)[lineno]
    cur_indent = len(cur_line) - len(cur_line.lstrip())
    maxcode = len(_cached_code(frame.f_code.co_filename))
    next_indent = cur_indent
    next_line = cur_line
    code = []
    while next_indent >= cur_indent:
        lineno += 1
        code.append(next_line)
        if lineno >= maxcode:
            break
        next_line = _cached_code(frame.f_code.co_filename)[lineno]
        next_indent = len(next_line) - len(next_line.lstrip())

    l_code = [l[cur_indent:] for l in code]
    _, choiceargs = _stub_rewrite_while_choice(l_code, frame)
    return "\n    ".join(l_code), lineno, choiceargs

def _trace_once(frame, event, arg):
    "Jump to line only available inside trace"
    # TODO: if line is function definition - run it normally
    #       and store its name
    #       to support locally-defined functions
    #print(event, frame, frame.f_lineno, frame.f_code.co_name)
    if not frame.f_code.co_name in ("__enter__", "__exit__", "orderedcontext"):
        code, lineno, choiceargs = _scan_to_exitcontext(frame)
        # print("Code:", _cached_code(frame.f_code.co_filename)[frame.f_lineno-1])
        # print("Full code:\n", code)
        # print("Would jump here to lineno", lineno + 1)
        frame.f_lineno = lineno + 1  # jump to after ordered context
        ctx_frame = frame
        sys.settrace(None)
        while frame:
            frame.f_trace = None  # not sure
            frame = frame.f_back
        # Compiling code happens here as there is no way to return to context manager
        full_function_code = f"def ordered_ctx_goal():\n    "+code
        #print("Full funciton code:")
        #print(full_function_code)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(code.encode("utf-8"))
            f_code = compile(full_function_code, fp.name, 'exec')
            exec(f_code, ctx_frame.f_locals)
            func = ctx_frame.f_locals["ordered_ctx_goal"]
            #print(ctx_frame.f_locals)
            hyperc.solve(func, choiceargs["functions"])
        global _dirty_is_context
        _dirty_is_context = False
    # return _trace
    return None

@contextmanager
def orderedcontext(*args, **kwds):
    "Partial context manager."
    #print("Enter context!")
    global _dirty_is_context
    _dirty_is_context = True
    sys.settrace(_trace_once)
    frame = sys._getframe().f_back
    while frame:
        frame.f_trace = _trace_once
        frame = frame.f_back
    yield None  # Due to code jump it never goes past yield

def choice(*args):
    if not _dirty_is_context: 
        raise RuntimeError("choice() is only allowed within ordered context")

def choices(*args):
    if not _dirty_is_context:
        raise RuntimeError("choices() is only allowed within ordered context")
