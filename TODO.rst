N   O    M    A   D    <>     T     O     D     O
-------------------------------------------------

Tidy up.
^^^^^^^^^

    #) Fix Plains.shift so that it creates a perfectly symmetrical
       octogon.


Implement weapons.
^^^^^^^^^^^^^^^^^^

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
