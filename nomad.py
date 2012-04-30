from entity import Entity

class Nomad(Entity):

    def __init__(self, los=5):
        super().__init__('nomad', False)
        self.los = los

    def move(self, plains, dx, dy):
        if not plains.walkable_at(self.x + dx, self.y + dy):
            return
        plains.shift(dx, dy)
        plains.move_fromto(self.x, self.y, self.x + dx, self.y + dy)


def move_nomad(dx, dy, nomad, plains):
    nomad.move(plains, dx, dy)
