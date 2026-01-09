from evennia import Command

class CmdMoon(Command):
    """
    Check the moons.

    Usage:
      moon

    Shows placeholder moon information (we'll replace with real calculations later).
    """
    key = "moon"
    aliases = ["moons"]
    locks = "cmd:all()"
    help_category = "World"

    def func(self):
        self.msg("|wThe moons above Tevethara|n")
        self.msg("  |rElarion|n (red moon): [placeholder phase/position]")
        self.msg("  |cSilthëa|n (blue moon): [placeholder phase/position]")
        self.msg("")
        self.msg("Tip: Later we'll tie this to your 1hr=1day clock + calendar system.")
