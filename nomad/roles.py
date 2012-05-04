from functools import wraps

MIN_SATIATION = 0
MAX_SATIATION = 100
MIN_HEALTH = 0
MAX_HEALTH = 100

SATIATION_DECAY = 0.25


class Role:

    def __init__(self):
        self.entity = None

    def assign(self, entity):
        self.entity = entity

    def __getattr__(self, *args, **kwargs):
        return getattr(self.entity, *args, **kwargs)

    def update(self, nomad):
        pass


class Matter(Role):

    def __init__(self, weight, edge):
        self.weight = weight
        self.edge = edge


class Edible(Role):

    def __init__(self, satiation, nutrition):
        super().__init__()
        self.satiation = satiation
        self.nutrition = nutrition


class Tool(Role):

    def __init__(self, on_use):
        super().__init__()
        self.on_use = on_use

    def use_on(self, entity):
        self.on_use(self, entity)


class Actor(Role):

    def __init__(self, action):
        super().__init__()
        self.action = action

    def update(self, nomad):
        self.action(self.entity, nomad)


class Reactor(Role):

    def __init__(self, action):
        super().__init__()
        self.action = action

    def react_to(self, entity):
        self.action(self.entity, entity)


class Mortal(Role):

    def __init__(self, satiation=MAX_SATIATION, health=MAX_HEALTH):
        super().__init__()
        self._satiation = satiation
        self._health = health

    def update(self, nomad):
        self.satiation -= SATIATION_DECAY

    @property
    def alive(self):
        return self.satiation > 0

    def _get_satiation(self):
        return self._satiation
    def _set_satiation(self, x):
        self._satiation = max(MIN_SATIATION, min(MAX_SATIATION, x))
    satiation = property(_get_satiation, _set_satiation)

    def _get_health(self):
        return self._health
    def _set_health(self, x):
        self._health = max(MIN_HEALTH, min(MAX_HEALTH, x))
    health = property(_get_health, _set_health)

    def eat(self, entity):
        '''Attempt to eat an entity. Return True if successful, else False.'''
        food = entity.as_food
        if food:
            self.satiation = self.satiation + food.satiation
            self.health = self.health + food.nutrition
            return True
        return False

    def eat_underfoot(self):
        '''Attempt to eat the entity underfoot.'''
        z, entity = self.get_underfoot()
        if self.eat(entity):
            self.plains.pop_entity(self.x, self.y, z)


class Tactile(Role):

    def __init__(self, tool_factory, left_held=None, right_held=None):
        super().__init__()
        self.tool_factory = tool_factory
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

    def put_underfoot(self, entity):
        if not entity:
            return
        z = self.plains.get_z(self.entity, self.entity.x, self.entity.y)
        self.plains.add_entity(entity, self.x, self.y, z)

    def drop_left(self):
        self.put_underfoot(self.left_held)
        self.left_held = None

    def drop_right(self):
        self.put_underfoot(self.right_held)
        self.right_held = None

    def drop_all(self):
        self.drop_left()
        self.drop_right()

    def make_tool(self):
        parts = frozenset(str(part) for part in
                          (self.left_held, self.right_held))

        if parts not in self.tool_factory:
            return

        if str(self.left_held) in parts:
            self.left_held = None
        if str(self.right_held) in parts:
            self.right_held = None
            
        tool = self.tool_factory[parts]()
        self.put_underfoot(tool)


