N   O    M    A   D    <>     T     O     D     O
-------------------------------------------------

Tidy up.
^^^^^^^^^

    #) Rewrite Plains.shift method.

    #) Comment roles.py.


Implement reach.
^^^^^^^^^^^^^^^^

    #) Write method Entity.in_reach.
       Yields the entity underfoot plus any adjacent, unwalkable
       entities.

    #) Change all Entity methods that operate on the entity underfoot to
       operate on the entity underfoot if possible, and otherwise to let
       the player select an adjacent entity with the cursor.


Implement weapons.
^^^^^^^^^^^^^^^^^^

    #) Write Tool subclass Weapon.
       Instead of taking an 'on_use' func, it takes params like damage,
       accuracy, etc. and defines it's own 'on_use'.

    #) Write Entity.damage method.
       Attempts to damage an entity, returning True if damage was dealt,
       False otherwise.

    #) Rename Tool to Usable, and Entity.as_tool to Entity.as_usable.

    #) Implement death for mortals and mulching for usable objects.

    #) Implement different mechanics for fleshy creatures and objects.
       Perhaps use the Matter role for this.


Implement hunting.
^^^^^^^^^^^^^^^^^^

    #) Implement corpses.
       When a fauna is killed, its corpse is left behind.
       A corpse can be cut while standing over it and wielding a sharp
       edge.

    #) Implement meat, hides and bones.
       When a corpse is cut, a stack of meat, hides and bones is left.
       Meat has high satiation. Hides can be used to make clothing and
       bags. Bones can be used to make a sharp edge.

    #) Write ``Mortal.throw`` method.
       Throws a held entity at a given target. Power and speed are
       determined by STR, and accuracy by AGL.
       Target selection mirrors Stone Soup's approach.
