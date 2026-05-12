"""
Non-player character typeclasses. NPCs are immobile, can't be picked up,
and respond to `talk <them>`.
"""

from typeclasses.objects import Object


class NPC(Object):
    """Base for non-player characters."""

    def at_object_creation(self):
        super().at_object_creation()
        self.locks.add("get:false()")

    def at_talk(self, talker):
        talker.msg(f"{self.key} has nothing to say.")


class BoatAttendant(NPC):
    """Ferry attendant in the Passenger Hold. Wakes new arrivals."""

    GREETING = (
        "|wThe ferry attendant taps your shoulder.|n \"Mind your things, "
        "friend — anything you brought down in the hold, grab it now. "
        "We're casting off again within the hour.\""
    )

    def at_talk(self, talker):
        talker.msg(self.GREETING)
