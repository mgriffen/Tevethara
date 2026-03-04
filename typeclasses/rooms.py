"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent

_BOX_WIDTH = 72  # total visual width of the ASCII box header


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    def get_display_name(self, looker=None, **kwargs):
        """Room name in brackets for inline references."""
        name = super().get_display_name(looker, **kwargs)
        return f"[{name}]"

    def return_appearance(self, looker, **kwargs):
        """Room appearance with box-draw ASCII header."""
        inner = _BOX_WIDTH - 2    # chars between ╔ and ╗  (70)
        content = inner - 2       # visible text width       (68)

        name = self.key

        # Collect exits in alphabetical order
        exits = sorted(
            [obj for obj in self.contents
             if hasattr(obj, "destination") and obj.destination],
            key=lambda e: e.key,
        )
        if exits:
            exits_text = "Exits: " + "  ".join(f"[{e.key}]" for e in exits)
        else:
            exits_text = "Exits: none"

        # Pad to fixed width (plain text only — room keys have no color codes)
        name_str  = name[:content].ljust(content)
        exits_str = exits_text[:content].ljust(content)

        top       = f"|x╔{'═' * inner}╗|n"
        name_line = f"|x║|n |y{name_str}|n |x║|n"
        sep       = f"|x╠{'═' * inner}╣|n"
        exit_line = f"|x║|n |c{exits_str}|n |x║|n"
        bottom    = f"|x╚{'═' * inner}╝|n"

        header = "\n".join([top, name_line, sep, exit_line, bottom])

        desc = self.db.desc or "|xThis place has no description yet.|n"

        # Visible non-exit contents
        visible = [
            obj for obj in self.contents
            if obj != looker
            and not (hasattr(obj, "destination") and obj.destination)
            and obj.access(looker, "view")
        ]
        chars  = [obj for obj in visible if obj.has_account]
        things = [obj for obj in visible if not obj.has_account]

        parts = [header, "", desc]
        if chars:
            parts.append("")
            parts.extend(
                f"  |w{ch.get_display_name(looker)}|n is here." for ch in chars
            )
        if things:
            parts.append("")
            parts.extend(f"  {th.get_display_name(looker)}" for th in things)

        return "\n".join(parts)
