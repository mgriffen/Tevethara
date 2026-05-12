from evennia import Command


class CmdUse(Command):
    """
    Use an item from your inventory.

    Usage:
      use <item>

    Calls the item's `at_use` hook. Items that don't define one will
    say so.
    """

    key = "use"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        if not self.args.strip():
            caller.msg("Use what?")
            return
        target = caller.search(self.args.strip(), location=caller, quiet=True)
        if not target:
            caller.msg(f"You aren't carrying anything called '{self.args.strip()}'.")
            return
        target = target[0] if isinstance(target, list) else target
        at_use = getattr(target, "at_use", None)
        if not callable(at_use):
            caller.msg(f"You can't use the {target.key}.")
            return
        at_use(caller)
