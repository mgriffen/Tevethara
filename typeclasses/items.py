"""
Item typeclasses. Stat values come from prototypes (world/prototypes/);
these classes carry shared in-game behavior.
"""

from evennia.utils.utils import delay

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


class Armor(Item):
    """
    Worn equipment. Slot is a tag (`feet`/`legs`/`chest`/...). `armor_value`
    is flat damage reduction applied before per-type resists.
    """

    pass


class Consumable(Item):
    """Items used up on activation. Subclasses define `at_use`."""

    def at_use(self, user):
        user.msg(f"You can't think of a way to use the {self.key}.")


class Bandage(Consumable):
    """
    Field bandage. Takes time to apply, can't be used in combat, consumed on
    successful application.
    """

    HEAL_AMOUNT = 15
    APPLY_TIME = 3.0

    def at_use(self, user):
        if user.db.in_combat:
            user.msg("|rYou can't bandage yourself in the middle of a fight.|n")
            return
        if user.db.applying_bandage:
            user.msg("You're already applying a bandage.")
            return
        user.db.applying_bandage = True
        user.msg("You begin wrapping a bandage around your wounds...")
        delay(self.APPLY_TIME, self._finish, user)

    def _finish(self, user):
        user.attributes.remove("applying_bandage")
        if not self.pk:
            return
        if user.db.in_combat:
            user.msg("|rThe bandaging is interrupted.|n")
            return
        hp = user.db.hp or 0
        hp_max = user.db.hp_max or 100
        new_hp = min(hp_max, hp + self.HEAL_AMOUNT)
        healed = new_hp - hp
        user.db.hp = new_hp
        if healed > 0:
            user.msg(f"|gYou finish bandaging. (+{healed} HP)|n")
        else:
            user.msg("You finish bandaging, but you weren't hurt to begin with.")
        self.delete()
