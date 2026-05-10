"""
Item typeclasses. Stat values come from prototypes (world/prototypes/);
these classes carry shared in-game behavior.
"""

from typeclasses.objects import Object


class Item(Object):
    """Common base for wieldable, wearable, and usable items."""

    pass


class Weapon(Item):
    """
    Weapons swing on the dual-timer model from Combat Core. Damage range,
    swing_time, accuracy, and crit_bonus are set by the spawning prototype.
    """

    pass
