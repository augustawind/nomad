from nomad.entity.fauna import Fauna

class Sentient(Fauna):

    def __init__(self, name, walkable, action, reaction=None,
                 left_held=None, right_held=None, **kwargs):
        super().__init__(name, walkable, action, reaction, **kwargs)
        self.left_held = left_held
        self.right_held = right_held

    def pickup_underfoot(self):
        z, entity = self.get_underfoot()
        if self.left_held is None:
            self.left_held = entity
        elif self.right_held is None:
            self.right_held = entity
        else:
            return
        self.plains.pop_entity(self.x, self.y, z)
