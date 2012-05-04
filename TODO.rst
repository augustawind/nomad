N   O    M    A   D    <>     T     O     D     O
-------------------------------------------------


Implement hatchet-making.
^^^^^^^^^^^^^^^^^^^^^^^^^

    #) Write a reed flora.

    #) Write an axe head entity.
       Make it: make_tool while holding a sharp rock in each hand.
       Consumes one of the rocks.

    #) Write an axe tool, to chop trees.
       Make it: make_tool while a reed, axe head, and stick are in
       any combination of your tool slots and underfoot.


Implement reach.
^^^^^^^^^^^^^^^^

    #) Write method Entity.in_reach.
       Yields the entity underfoot plus any adjacent, unwalkable
       entities.

    #) Change all Entity methods that operate on the entity underfoot to
       operate on the entity underfoot if possible, and otherwise to let
       the player select an adjacent entity with the cursor.


Implement hunting.
^^^^^^^^^^^^^^^^^^

    #) Write ``Fauna.throw`` method.
       Throws a held entity at a given target. Power and speed are
       determined by STR, and accuracy by AGL.
       Target selection mirrors Stone Soup's approach.

    #) Implement corpses.
       When a fauna is killed, its corpse is left behind.
       A corpse can be cut while standing over it and wielding a sharp
       edge.

    #) Implement meat, hides and bones.
       When a corpse is cut, a stack of meat, hides and bones is left.
       Meat has high satiation. Hides can be used to make clothing and
       bags. Bones can be used to make a sharp edge.
