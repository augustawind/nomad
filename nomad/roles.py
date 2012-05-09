'''entity behaviors'''
from functools import wraps

class Role:
    '''Abstract class for `Entity` behaviors.'''

    def __init__(self):
        self.entity = None

    def assign(self, entity):
        '''Assign this role to an entity.'''
        self.entity = entity

    def __getattr__(self, *args, **kwargs):
        '''If an attribute is not found on the role, search its entity.

        A role must be assigned with `Role.assign` before this will work.
        '''
        return getattr(self.entity, *args, **kwargs)

    def update(self, nomad):
        '''Update the entity assigned to this role, given a `Nomad`.
        
        This method is called each turn of the game.
        '''
        pass


class Matter(Role):
    '''Something with physical properties.'''

    def __init__(self, weight, edge):
        self.weight = weight
        self.edge = edge


class Edible(Role):
    '''Something that can be eaten, for good or ill.'''

    def __init__(self, satiation, nutrition):
        super().__init__()
        self.satiation = satiation
        self.nutrition = nutrition


class Tool(Role):
    '''Something that can be "used" on another Entity.'''

    def __init__(self, on_use):
        super().__init__()
        self.on_use = on_use

    def use_on(self, entity):
        '''Use the tool on another entity.'''
        self.on_use(self, entity)


class Actor(Role):
    '''Something that acts each turn.'''

    def __init__(self, action):
        super().__init__()
        self.action = action

    def update(self, nomad):
        '''Perform an action.'''
        self.action(self.entity, nomad)


class Reactor(Role):
    '''Something that reacts when engaged with.'''

    def __init__(self, action):
        super().__init__()
        self.action = action

    def react_to(self, entity):
        '''Perform an action in response to an Entity.'''
        self.action(self.entity, entity)


class Mortal(Role):
    '''Something that can die and requires sustainance to stay alive.'''

    MIN_SATIATION = 0
    MAX_SATIATION = 100
    MIN_HEALTH = 0
    MAX_HEALTH = 100

    SATIATION_DECAY = 0.25

    def __init__(self, satiation=MAX_SATIATION, health=MAX_HEALTH):
        super().__init__()
        self._satiation = satiation
        self._health = health

    def update(self, nomad):
        '''Reduce satiation by a fixed amount.'''
        self.satiation -= self.SATIATION_DECAY

    @property
    def alive(self):
        '''Is the mortal alive?'''
        return self.satiation > 0

    def _get_satiation(self):
        return self._satiation
    def _set_satiation(self, x):
        self._satiation = max(self.MIN_SATIATION, min(self.MAX_SATIATION, x))
    satiation = property(_get_satiation, _set_satiation, doc=
        'How full is the mortal? If this reaches 0, death occurs.')

    def _get_health(self):
        return self._health
    def _set_health(self, x):
        self._health = max(self.MIN_HEALTH, min(self.MAX_HEALTH, x))
    health = property(_get_health, _set_health, doc=
        'How healthy is the mortal? If this reaches 0, death occurs.')

    def eat(self, entity):
        '''Attempt to eat an entity. Return True if successful, else False.'''
        food = entity.as_food
        if food:
            self.satiation = self.satiation + food.satiation
            self.health = self.health + food.nutrition
            return True
        return False

    def eat_nearest(self):
        entities = self.get_accessable()
        z, entity = entities.popitem(last=False)
        if self.eat(entity):
            self.plains.pop_entity(self.entity.x, self.entity.y, z)


class Tactile(Role):
    '''Something that has fine motor control.'''

    def __init__(self, tool_factory, left_held=None, right_held=None):
        super().__init__()
        self.tool_factory = tool_factory
        self.left_held = left_held
        self.right_held = right_held

    def pickup_nearest(self):
        entities = self.get_accessable()
        z, entity = entities.popitem(last=False)
        if self.left_held is None:
            self.left_held = entity
        elif self.right_held is None:
            self.right_held = entity
        else:
            return
        self.plains.pop_entity(self.entity.x, self.entity.y, z)

    def drop_left(self):
        '''Drop the entity in the tactile's left hand underfoot.'''
        self.put_underfoot(self.left_held)
        self.left_held = None

    def drop_right(self):
        '''Drop the entity in the tactile's right hand underfoot.'''
        self.put_underfoot(self.right_held)
        self.right_held = None

    def drop_all(self):
        '''Drop all entities held by the tactile.'''
        self.drop_left()
        self.drop_right()

    def make_tool(self):
        '''Attempt to make a tool with the entities on hand.'''
        parts = frozenset(str(part) for part in
                          (self.left_held, self.right_held))

        if parts not in self.tool_factory:
            return

        min_intelligence, tool = self.tool_factory[parts]
        if self.stats.intelligence < min_intelligence:
            return

        if str(self.left_held) in parts:
            self.left_held = None
        if str(self.right_held) in parts:
            self.right_held = None
            
        self.put_underfoot(tool())
