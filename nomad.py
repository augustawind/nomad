from entity import Entity

class Nomad(Entity):

    def __init__(self, los=5):
        super().__init__('nomad', False)
        self.los = los

    def move(self, plains, dx, dy):
        plains.shift(dx, dy)
        super().move(plains, dx, dy)


def move_nomad(dx, dy, nomad, plains):
    nomad.move(plains, dx, dy)
