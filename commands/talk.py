from evennia import Command


class CmdTalk(Command):
    """
    Talk to someone in the room.

    Usage:
      talk <target>

    Calls the target's `at_talk` hook. Things that don't define one will
    say so.
    """

    key = "talk"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        query = self.args.strip()
        if not query:
            self.caller.msg("Talk to whom?")
            return
        target = self.caller.search(query)
        if not target:
            return
        at_talk = getattr(target, "at_talk", None)
        if not callable(at_talk):
            self.caller.msg(f"{target.key} has nothing to say.")
            return
        at_talk(self.caller)
