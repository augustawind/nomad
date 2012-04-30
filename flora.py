from entity import *

def grass(): return Entity("grass", True)
def flower(): return Entity("flower", True)
def mushroom(): return Entity("mushroom", True, 'flora', as_food=defaultFood)
