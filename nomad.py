from entity import Entity

class Nomad(Entity):

    def __init__(self, los=5):
        super().__init__('nomad', False)
        self.los = los

    def move(self, dx, dy):
        if not self.plains.walkable_at(self.x + dx, self.y + dy):
            return
        self.plains.shift(dx, dy)
        self.plains.move_fromto(self.x, self.y, self.x + dx, self.y + dy)


def move_nomad(dx, dy, nomad):
    nomad.move(dx, dy)
