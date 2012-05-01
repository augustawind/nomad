from nomad.entity.sentient import Sentient
from nomad.entity.fauna.actions import idle

class Nomad(Sentient):

    def __init__(self, los=5):
        super().__init__('nomad', False, idle())
        self.los = los

    def move(self, dx, dy):
        if not self.plains.walkable_at(self.x + dx, self.y + dy):
            return
        self.plains.shift(dx, dy)
        self.plains.move_fromto(self.x, self.y, self.x + dx, self.y + dy)
