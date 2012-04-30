FAUNA = 1

class Entity:
    '''A thing that exists in the plains.'''

    def __init__(self, name, walkable, etype='entity'):
        self.name = name
        self.walkable = walkable
        self.etype = etype

        self.x = None
        self.y = None
        self.plains = None

    def update(self, nomad):
        '''Move the entity a step forward in time. Does nothing, but
        subclasses can override this method to provide behavior.
        '''
        pass

    def move(self, dx, dy):
        '''Move the entity in the given direction on its plains.'''
        assert None not in (self.x, self.y, self.plains)
        x = self.x + dx
        y = self.y + dy
        if not self.plains.walkable_at(x, y):
            return
        self.plains.move_fromto(self.x, self.y, x, y) 
