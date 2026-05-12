from evennia import Command


_SLOT_DISPLAY_ORDER = [
    "head", "neck", "shoulders", "chest", "back", "wrists",
    "hands", "waist", "legs", "feet", "finger_l", "finger_r",
    "main_hand", "off_hand", "ranged", "trinket",
]


def _resolve(caller, query):
    """Find an item in the caller's inventory by name/alias."""
    matches = caller.search(query, location=caller, quiet=True)
    if not matches:
        return None
    return matches[0] if isinstance(matches, list) else matches


class CmdEquip(Command):
    """
    Equip an item from your inventory.

    Usage:
      equip <item>
      wear <item>
      wield <item>

    The item is placed in whatever slot its design calls for. If something
    is already in that slot, it is removed automatically.
    """

    key = "equip"
    aliases = ["wear", "wield"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        query = self.args.strip()
        if not query:
            self.caller.msg(f"{self.cmdstring.capitalize()} what?")
            return
        target = _resolve(self.caller, query)
        if not target:
            self.caller.msg(f"You aren't carrying anything called '{query}'.")
            return
        self.caller.equip(target)


class CmdUnequip(Command):
    """
    Remove an equipped item.

    Usage:
      unequip <item>
      remove <item>
    """

    key = "unequip"
    aliases = ["remove"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        query = self.args.strip()
        if not query:
            self.caller.msg(f"{self.cmdstring.capitalize()} what?")
            return
        target = _resolve(self.caller, query)
        if not target:
            self.caller.msg(f"You aren't carrying anything called '{query}'.")
            return
        self.caller.unequip(target)


class CmdEquipment(Command):
    """
    Show what you have equipped.

    Usage:
      equipment
      eq
    """

    key = "equipment"
    aliases = ["eq"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        equipped = self.caller.db.equipped or {}
        if not equipped:
            self.caller.msg("You have nothing equipped.")
            return
        lines = ["|wEquipped:|n"]
        seen = set()
        for slot in _SLOT_DISPLAY_ORDER:
            item = equipped.get(slot)
            if item is not None:
                lines.append(f"  |x{slot:>10}|n  {item.key}")
                seen.add(slot)
        for slot, item in equipped.items():
            if slot not in seen:
                lines.append(f"  |x{slot:>10}|n  {item.key}")
        self.caller.msg("\n".join(lines))
