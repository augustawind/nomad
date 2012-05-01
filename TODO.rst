N   O    M    A   D    <>     T     O     D     O
-------------------------------------------------


Implement tools and toolmaking.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #) Write ``Bipedal.make_tool`` method.
       Attempts to make a tool with one or two held entities and/or the
       entity underfoot.

    #) Write ``Tool`` deriving from entity.
       Tools can be used to interact with entities on the plains in
       different ways.

    #) Write a spear tool that serves as a general purpose edge
       (and could forseeably be useful as a weapon too).

    #) Write 'stick' and 'sharp rock' entities.
       Calling ``make_tool`` while holding the rock and standing on
       the stick returns a spear.


Implement hatchet-making.
^^^^^^^^^^^^^^^^^^^^^^^^^

    #) Write a vine flora.

    #) Write an axe head entity.
       Make it: make_tool while holding a sharp rock in each hand.
       Consumes one of the rocks.

    #) Write an axe tool, to chop trees.
       Make it: make_tool while a vine, axe head, and stick are in
       any combination of your tool slots and underfoot.


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
