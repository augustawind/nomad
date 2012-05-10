'''entity behaviors'''
from collections import OrderedDict

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
    
    def damage(self, dmg):
        '''Cause damage to the entity assigned to this role.
        
        Return True if damage was dealt, else False.
        '''
        return False


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


class Usable(Role):
    '''Something that can be "used" on another Entity.'''

    def __init__(self, on_use):
        super().__init__()
        self.on_use = on_use

    def use_on(self, entity):
        '''Use the usable on another entity.'''
        self.on_use(self, entity)


class Weapon(Role):
    '''A tool for killing.'''

    def __init__(self, damage, accuracy, nhits):
        self.damage = damage
        self.accuracy = accuracy
        self.nhits = nhits

    def use_on(self, entity):
        for i in range(self.nhits):
            if random() * 100 > self.accuracy:
                continue
            entity.damage(self.damage)


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

    def damage(self, dmg):
        if not self.health:
            return False
        self.health -= dmg
        return True

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
        edible = entity.as_edible
        if edible:
            self.satiation = self.satiation + edible.satiation
            self.health = self.health + edible.nutrition
            return True
        return False

    def eat_nearest(self):
        entity = self.select_in_reach()
        if entity and self.as_mortal.eat(entity):
            self.plains.remove_entity(entity)


class Tactile(Role):
    '''Something that has fine motor control.'''

    def __init__(self, object_factory, left_held=None, right_held=None):
        super().__init__()
        self.object_factory = object_factory
        self.held_entities = [left_held, right_held]

    def assign(self, entity):
        super().assign(entity)

    def eat_nearest(self):
        for i, entity in enumerate(self.held_entities):
            if entity and self.as_mortal.eat(entity):
                self.held_entities[i] = None
                return
        self.as_mortal.eat_nearest()

    def pickup_nearest(self):
        # Get closest entity in reach.
        entity = self.select_in_reach()

        # Quit if entity unmoveable.
        if not entity or not entity.moveable:
            return

        # Put entity in a free hand, or quit if there isn't one.
        if self.held_entities[0] is None:
            self.held_entities[0] = entity
        elif self.held_entities[1] is None:
            self.held_entities[1] = entity
        else:
            return

        # Remove the entity from the plains.
        self.plains.remove_entity(entity)

    def drop_left(self):
        '''Drop the entity in the tactile's left hand underfoot.'''
        self.put_underfoot(self.held_entities[0])
        self.held_entities[0] = None

    def drop_right(self):
        '''Drop the entity in the tactile's right hand underfoot.'''
        self.put_underfoot(self.held_entities[1])
        self.held_entities[1] = None

    def drop_all(self):
        '''Drop all entities held by the tactile.'''
        self.drop_left()
        self.drop_right()

    def combine_objects(self):
        '''Attempt to make a usable with the entities on hand.'''
        parts = frozenset(part.name for part in self.held_entities if part)

        if parts not in self.object_factory:
            return

        min_intelligence, usable = self.object_factory[parts]
        if self.stats.intelligence < min_intelligence:
            return

        for i, part in enumerate(self.held_entities):
            if part.name() in parts:
                self.held_entities[i] = None
            
        self.put_underfoot(usable())
