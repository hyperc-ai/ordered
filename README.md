
# Python module `ordered`

`ordered` module is the opposite to `random` - it maintains order in the program

## _`ordered`_.`choice()` method

### Synopsis:

- _ordered_.**choice**(objects=None)
 
   Return the object that maintains maximum order in the program (minimum entropy). Any exception increases entropy to infinity.

    `objects` is a list of objects to choose from. If `objects` is None then gc.get_objects() is assumed by default.

    Raises `SchedulingError` if it was not able to find an exit at all. It might require unexpected amount of resources, in which case additional training of the core model is required.

    **Warning:** not all Python features are currently supported and order might fail with internal exception. In this case a rewrite of the code is needed to remove the usage of unsupported features (such as I/O, lists and for loops.)

### Examples:

```python
import ordered

data = 5

def increase():
    data += 1

def decrease():
    data -= 1

while data != 10: ordered.choice()()
```

This will exit the program after running increase() 5 times. `choice` searches for the fastest way to exit the context in which it is located.

## Work-in-progress methods

### Method _`ordered`_.`relaxedchoice(objects=None)`

Guaranteed to find an exit. Modifies the program if required.

### Method _`ordered`_.`def(heap_in_out: List)`

Defines a function from a list of input and output heaps. The more examples of heaps are supplied, the better is the function.



