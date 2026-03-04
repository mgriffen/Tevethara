"""
Map builder command.
"""

from commands.command import Command


class CmdMapSet(Command):
    """
    Set or inspect map coordinates on the current room.

    Usage:
        @mapset <area> <x> <y>   - tag this room with coordinates
        @mapset/show             - show this room's current coordinates
        @mapset/clear            - remove coordinates from this room

    Examples:
        @mapset oasmc 0 10
        @mapset ferry 0 1
        @mapset/show
        @mapset/clear

    Coordinate convention:
        east = +x, west = -x, north = +y, south = -y

    Area names in use:
        oasmc         - the full OASMC island (compliance + academy)
        ferry         - the crossing vessel
        understructure - sealed lower levels
        faculty_tower  - restricted upper tower
    """

    key = "@mapset"
    aliases = ["@mapedit"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"

    def func(self):
        # Parse /switch from args (base Command doesn't do this automatically)
        # e.g. "@mapset/show" → self.args = "/show"
        switches = []
        args = self.args.strip()
        if args.startswith("/"):
            switch_part, _, args = args[1:].partition(" ")
            switches = [switch_part.lower()]
        self.args = args

        room = self.caller.location
        if not room:
            self.caller.msg("You have no location.")
            return

        if "clear" in switches:
            room.db.map_area = None
            room.db.map_x = None
            room.db.map_y = None
            self.caller.msg(f"Cleared map coordinates from [{room.key}].")
            return

        if "show" in switches or not self.args.strip():
            area = room.db.map_area
            x = room.db.map_x
            y = room.db.map_y
            if area is None:
                self.caller.msg(f"[{room.key}]: no map coordinates set.")
            else:
                self.caller.msg(f"[{room.key}]: area={area}  x={x}  y={y}")
            return

        parts = self.args.strip().split()
        if len(parts) != 3:
            self.caller.msg("Usage: @mapset <area> <x> <y>")
            return

        area, x_str, y_str = parts
        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            self.caller.msg("x and y must be integers.")
            return

        room.db.map_area = area
        room.db.map_x = x
        room.db.map_y = y
        self.caller.msg(f"[{room.key}]: area={area}  x={x}  y={y}")
