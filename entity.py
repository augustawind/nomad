FAUNA = 1

class Entity:

    def __init__(self, name, walkable, etype='entity'):
        self.name = name
        self.walkable = walkable
        self.etype = etype
        self.x = None
        self.y = None

    def update(self, nomad, plains):
        return NotImplemented

    def move(self, plains, dx, dy):
        assert None not in (self.x, self.y)
        x = self.x + dx
        y = self.y + dy
        if not plains.walkable_at(x, y):
            return
        plains.move_fromto(self.x, self.y, x, y) 
