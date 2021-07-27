[![alt text][1.1]][1]
[![alt text][2.1]][2]

[1.1]: http://i.imgur.com/tXSoThF.png (HyperC on twitter)
[2.1]: http://i.imgur.com/P3YfQoD.png (HyperC on facebook)

[1]: https://twitter.com/hyperc_ai
[2]: https://www.facebook.com/HyperComputation/

# Python module `ordered`

`ordered` module is the opposite to `random` - it maintains order in the program.

## _`ordered`_.`choice()` method

- _ordered_.**choice**(objects=None)
 
   Choose and return the object that maintains maximum order in the program (minimum entropy). Any exception increases entropy to infinity so choices leading to exceptions will be avoided.

    `objects` is a list of objects to choose from. If `objects` is `None` then `gc.get_objects()` is assumed by default.

    Raises `SchedulingError` if it was not able to find an exit at all. Large problems might require unexpected amount of resources in which case additional training of the core model is required.

    _**Warning:** not all Python features are currently supported and thus `ordered` might fail with internal exception. In this case a rewrite of user code is needed to remove the usage of unsupported features (such as I/O, lists and for loops.)_
    
    _**Warning:** `ordered` requires all entropy-controlled code to be type-hinted._

## Entropy Context Objects

Contexts are environments of controlled entropy. Entropy contexts allow you to control which portions of the program will be guaranteed to exit with minimum state-changing steps. By default, the entire program till the end is considered to be a controlled context.

- _ordered_.**orderedcontext**()

  Return a context manager that will set the current context for the active thread to a copy of ctx on entry to the with-statement and restore the previous context when exiting the with-statement. If no context is specified, a copy of the current context is used. `SchedulingError` will be raised if exit is not possible.
  
  Context allows to set parameters and limits such as `timeout` and `max_memory`.
  
  Inside a context only objects defined within this context are considered by `ordered.choice()` by default instead of `gc.get_objectx()`.

  For example, the following code executes a portion of the program in an entropy-controlled context:
  
```python
import ordered
step_count = 0
with ordered.orderedcontext() as ctx:
    ctx.timeout = 10  # 10 seconds max time to find a solution
    x = 0
    while ordered.choice([True, False]):
        x = ordered.choice([lambda: x + 9, lambda: x - 1])()
        step_count += 1
    assert x == 15
open("result.txt", "w+").write(f"x={x}, steps={step_count}")  # x equals 15
```

## Examples:

### Primitive increase

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

### Pouring problem

A classic bottle pouring puzzle. You are in the possession of two bottles, one with a capacity of 3 litres and one with a capacity of 5 litres. Next to you is an infinitely large tub of water. You need to measure exactly 4 litres in one of the bottles. You are only allowed to entirely empty or fill the bottles. You can't fill them partially since there is no indication on the bottles saying how much liquid is in them. How do you measure exactly 4 litres?

```python
from ordered import orderedcontext, choice
with orderedcontext():
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
        if self.fill <= can_fit:
            bottle.fill += self.fill
            self.fill = 0
            assert self.fill == 0
            assert bottle.fill == bottle.fill + self.fill
        else:
            bottle.fill += can_fit
            self.fill -= can_fit
            assert bottle.fill == bottle.volume
            assert self.fill == self.fill - can_fit
    def empty(self):
        self.fill = 0
        assert self.fill == 0
  b1 = Bottle(3)
  b2 = Bottle(5)
  while b2.fill != 4: 
      choice([Bottle.fill_in, Bottle.pour_out, Bottle.empty])(choice([b1,b2]))
```

### Learning a function

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

### Method _`ordered`_.`relaxedchoice(objects=None)`

Guaranteed to find an exit. Modifies the program if required.

### Method _`ordered`_.`def(heap_in_out: List)`

Defines a function from a list of input and output heaps. The more examples of heaps are supplied, the better is the function.

# Credits

Module `ordered` is developed and maintained by HyperC team, https://hyperc.com (CriticalHop Inc.)

