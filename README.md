[![alt text][1.1]][1]
[![alt text][2.1]][2]

[1.1]: http://i.imgur.com/tXSoThF.png (HyperC on twitter)
[2.1]: http://i.imgur.com/P3YfQoD.png (HyperC on facebook)

[1]: https://twitter.com/hyperc_ai
[2]: https://www.facebook.com/HyperComputation/

# Python module `ordered`

`ordered` module is the opposite to `random` - it maintains order in the program.


```python
import random 
x = 5
def increase():
    global x
    x += 7
def decrease():
    global x
    x -= 2

while x != 22:  
    random.choice([increase, decrease])()  
    # takes long time to exit ...
```
vs.

```python
import random, ordered
x = 5
def increase():
    global x
    x += 7
def decrease():
    global x
    x -= 2

with ordered.orderedcontext(): # entropy-controlled context
    while x != 22: 
        random.choice([increase, decrease])()  
    # exits immediately with correct result
```

# Usage

Just run your program. `ordered` has a significant "warm-up" time which includes several stages of logic order lowering.

```
pip install ordered
```

## Entropy Context Objects

```python
# ... normal python code
with ordered.orderedcontext():  
    # ... entropy-controlled context
# ... normal python code
```

Ordered contexts are environments of controlled entropy. Contexts allow you to control which portions of the program will be guaranteed to exit with minimum state-changing steps. Raising any exceptions is also avoided by providing the correct "anti-random" `choice()` results. 

- _ordered_.**orderedcontext**()

  Return a context manager and enter the context. `SchedulingError` will be raised if exit is not possible.
  
  Inside ordered context functions `random.choice` and `ordered.choice` are equivalent and no randomness is possible. If `choice()` is called without parameters then `gc.get_objects()` (all objects in Python heap) is considered by default.

  Optional returned context object allows to set parameters and limits such as `timeout` and `max_states`.
  
    _**Warning:** not all Python features are currently supported and thus `ordered` might fail with internal exception. In this case a rewrite of user code is needed to remove the usage of unsupported features (such as I/O, lists and for loops.)_
    
    _**Warning:** `ordered` requires all entropy-controlled code to be type-hinted._

```python
# ...
def decrease():
    global x
    assert x > 25  # when run inside context this excludes cases when x <= 25
                   # thus increasing amount of overall steps needed to complete
    x -= 2
# ...
with ordered.orderedcontext(): # entropy-controlled context
    while x < 21:  # exit if x >= 21
        random.choice([increase, decrease])()  
    assert x < 23  # only x == 21 or 22 matches overall
```

## _`ordered`_.`choice()` method

- _ordered_.**choice**(objects=None)
 
   Choose and return the object that maintains maximum order in the program (minimum entropy). Any exception increases entropy to infinity so choices leading to exceptions will be avoided.
   Inside the entropy controlled context, `random.choice` is equivalent to `ordered.choice`.

    `objects` is a list of objects to choose from. If `objects` is `None` then `gc.get_objects()` is assumed by default.

    _**Warning:** current implementation of `while ... ordered` loop is hard-coded to the form shown in examples. `while` loops with other statements than a single-line `choice()` are not supported. Add your code to other parts of context and/or functions and methods in your program_


## _`ordered`_.`side_effect(lambda: <code>)` method

- _ordered_.**side_effect**(lamdba=[lambda function])

    Execute the supplied lambda function as a side-effect avoiding the compilation and subsequent effect analysis by `ordered`. This is useful when I/O is easier schdeuled right within the entropy-controlled part of the program or when you know that the code to be executed has no useful effect on the state of the problem of interest.

    ```python
    def move(t: Truck, l: Location):
        "Move truck to any adjacent location"
        assert l in t.location.adjacent
        t.locaiton = l
        t.distance += 1
        side_effect(lambda: print(f"This {__name__} code can have any Python construct and is not analysed. Current value is {t.distance}"))
    ```

## Examples:

### Object Oriented Code

Preferred way of implementing software models with `ordered` is object-oriented:

```python
import ordered

class MyVars:
    x: int
    steps: int
    def __init__(self) -> None:
        self.x = 0
        self.steps = 0

    def plus_x(self):
        self.x += 3
        self.count_steps()

    def minus_x(self):
        self.x -= 2
        self.count_steps()
    
    def count_steps(self):
        self.steps += 1

m = MyVars()
m.x = 5
with ordered.orderedcontext():
    while m.x != 12:  
        ordered.choice()()  

print("Steps:", steps)
```


### Pouring problem

A classic bottle pouring puzzle. You are in the possession of two bottles, one with a capacity of 3 litres and one with a capacity of 5 litres. Next to you is an infinitely large tub of water. You need to measure exactly 4 litres in one of the bottles. You are only allowed to entirely empty or fill the bottles. You can't fill them partially since there is no indication on the bottles saying how much liquid is in them. How do you measure exactly 4 litres?

```python
from ordered import orderedcontext, choice
class Bottle:
    volume: int
    fill: int
    def __init__(self, volume: int):
        self.volume = volume
        self.fill = 0
    def fill_in(self):
        self.fill += self.volume
        assert self.fill == self.volume
    def pour_out(self, bottle: "Bottle"):
        assert self != bottle
        can_fit = bottle.volume - bottle.fill
        sf = self.fill
        bf = bottle.fill
        if self.fill <= can_fit:
            bottle.fill += self.fill
            self.fill = 0
            assert self.fill == 0
            assert bottle.fill == bf + sf
        else:
            bottle.fill += can_fit
            self.fill -= can_fit
            assert bottle.fill == bottle.volume
            assert self.fill == sf - can_fit
    def empty(self):
        self.fill = 0
b1 = Bottle(3)
b2 = Bottle(5)
with orderedcontext():
  while b2.fill != 4: 
      choice([Bottle])()
pass
```

_**NOTE:** Be careful with importing from a module into global namespace and using `choice()()` without parameters in global scope. Current implementation load all global objects including the `orderedcontext` and `choice` and cause an error_

### Learning a function

`ordered` can be used 

```python
from ordered import choice, orderedcontext
from dataclasses import dataclass 

@dataclass
class Point:
   x: int
   y: int
   
data = [Point(1,1), Point(2,4), Point(3,9)]

# TODO: create_function creates a nonrandom function out of Node objects with `ordered.choice`
# TODO: run_function runs a node tree with a value and returns result
    
with orderedcontext():
    f = create_function()
    for point in data:
        assert run_function(f, point.x) == point.y
# context exit guarantees that create_function() constructs a correct function to describe input

# TODO: approximate function learning example
```

## Work-in-progress methods

### _`ordered`_.`relaxedcontext()`

Guaranteed to find an exit. Modifies the program if required.

### Method _`ordered`_.`def(heap_in_out: List)`

Defines a function from a list of input and output heaps. The more examples of heaps are supplied, the better is the function.

# Status

Although the system is in use by several industry organizations, `ordered` is under heavy development. Expect rapid changes in language support, performance and bugs. 

# Limitations

## Python Language

Overall we have a relatively complete support of 'basic' use of object-oriented programming style. However, there are some hard limitaions and work-in-progress items that are yet to be documented.

Try to avoid multiline code as we have several places where line continuation may break during compilation.

Built-ins support is minimal. No I/O can be executed except for in explicit `side_effect()` calls. 

None of the "ordered data structures" are supported: this includes `list`, `dict` and `tuple`. Use `set` or create your own data structures based on objects and classes.

Loops are not supported, including `while` and `for` besides the main `while..choice()` loop as described above - define your problem by creating functions that can be iteratively called by `while.. choice()` to overcome this.

Support of missing features is a current work in progress.

## Integer Math

Math implementation is simple and works up to count 20-50 depedning on available resources. Future development includes switching to register-based math and monotonic-increase heuristics to support any numbers. 

## Symbolic Execution Performance

Current implementaion of Python code compilation is naive and doesn't scale well. The simpler your code, the faster it will compile. Future development includes implementing smarter symboic execution heuristics, pre-calculated database and statistical methods.

## Model Universality

Current model can efficiently handle a limited set of problem classes and might require significantly more resources than would be needed with a more complete model. HyperC team provides more complete models for specific industry per request. Future development includes adding a universal pruning based on statistical methods as amount of data available to HyperC team grows.

# Science behind `ordered`

`ordered` is based on translating a Python program to [AI planning](https://en.wikipedia.org/wiki/Automated_planning_and_scheduling) problem and uses a customized [fast-downward](http://www.fast-downward.org/) as a backend. Additionally, we're implementing machine learning and pre-computed matrices on various levels to vastly improve performance on larger problems.

# Credits

Module `ordered` is developed and maintained by HyperC team, https://hyperc.com (CriticalHop Inc.)

For any questions and inquries please contact Andrew Gree, <andrewg@hyperc.com>.

# Investor Relations

HyperC is fundraising! Please contact at <andrewg@hyperc.com>.