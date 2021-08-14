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