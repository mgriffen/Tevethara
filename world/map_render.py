"""
ASCII map renderer for Tevethara.

Room coordinate attributes:
    room.db.map_x    = int   (east = +, west = -)
    room.db.map_y    = int   (north = +, south = -)
    room.db.map_area = str   (area name, e.g. "oasmc", "ferry")

Map symbols:
    @  = player's current room
    #  = regular room
    ^  = has a cross-area exit leading "up" (up, climb, ladder...)
    v  = has a cross-area exit leading "down" (down, hatch, descend...)
    *  = has both up- and down-type cross-area exits
    -  = east/west corridor
    |  = north/south corridor
"""

from evennia.utils.search import search_objects_by_typeclass

# Cardinal directions: exit key -> (dx, dy)
CARDINAL = {
    "north": (0, 1),  "n": (0, 1),
    "south": (0, -1), "s": (0, -1),
    "east":  (1, 0),  "e": (1, 0),
    "west":  (-1, 0), "w": (-1, 0),
}

# Exit names that indicate cross-area vertical movement
UP_EXITS   = frozenset({"up", "u", "climb", "ascend", "ladder", "upstairs", "above"})
DOWN_EXITS = frozenset({"down", "d", "descend", "hatch", "downstairs", "below"})

# Viewport half-extents in room-space.
# Total visible: (VP_H*2+1) rooms wide, (VP_V*2+1) rooms tall.
# Character grid: (VP_H*4+1) wide, (VP_V*4+1) tall.
VP_H = 5   # 11 rooms wide  → 21 chars
VP_V = 3   # 7 rooms tall   → 13 chars


def _get_area_rooms(area_name):
    """Return {(x, y): room} for all tagged rooms in the named area."""
    rooms = search_objects_by_typeclass("typeclasses.rooms.Room")
    result = {}
    for room in rooms:
        if (room.db.map_area == area_name
                and room.db.map_x is not None
                and room.db.map_y is not None):
            result[(int(room.db.map_x), int(room.db.map_y))] = room
    return result


def _room_symbol(room, player_room):
    """Return the single-character map symbol for this room."""
    if room == player_room:
        return "@"

    has_up = has_down = False
    for ex in room.exits:
        ek = ex.key.lower()
        dest = ex.destination
        if not dest:
            continue
        # Cross-area exit?
        if dest.db.map_area != room.db.map_area:
            if ek in UP_EXITS:
                has_up = True
            elif ek in DOWN_EXITS:
                has_down = True

    if has_up and has_down:
        return "*"
    if has_up:
        return "^"
    if has_down:
        return "v"
    return "#"


def render_area_map(player_room):
    """
    Render an ASCII map of the player's current area, centered on the player.
    Returns a plain string (no ANSI codes) for display in a <pre> element.
    Returns a short status string if the room has no map data.
    """
    area = getattr(player_room.db, "map_area", None)
    if not area:
        return "[ No map data ]"

    px = player_room.db.map_x
    py = player_room.db.map_y
    if px is None or py is None:
        return "[ Room not mapped ]"

    px, py = int(px), int(py)

    coord_map = _get_area_rooms(area)
    if not coord_map:
        return "[ No map data ]"

    # Viewport bounds in room-space
    rx_min, rx_max = px - VP_H, px + VP_H
    ry_min, ry_max = py - VP_V, py + VP_V

    # Character grid: rooms at even indices, corridors at odd indices.
    # Width = (rx_max - rx_min)*2 + 1,  Height = (ry_max - ry_min)*2 + 1
    gw = (rx_max - rx_min) * 2 + 1
    gh = (ry_max - ry_min) * 2 + 1
    grid = [[" "] * gw for _ in range(gh)]

    def gx(rx):
        return (rx - rx_min) * 2

    def gy(ry):
        # Invert Y so that north = up on screen
        return (ry_max - ry) * 2

    # Place room symbols
    for (rx, ry), room in coord_map.items():
        if rx_min <= rx <= rx_max and ry_min <= ry <= ry_max:
            grid[gy(ry)][gx(rx)] = _room_symbol(room, player_room)

    # Draw corridor connectors
    for (rx, ry), room in coord_map.items():
        if not (rx_min <= rx <= rx_max and ry_min <= ry <= ry_max):
            continue
        cx, cy = gx(rx), gy(ry)
        for ex in room.exits:
            ek = ex.key.lower()
            if ek not in CARDINAL:
                continue
            dx, dy = CARDINAL[ek]
            neighbor = coord_map.get((rx + dx, ry + dy))
            if not neighbor:
                continue
            nx, ny = rx + dx, ry + dy
            if not (rx_min <= nx <= rx_max and ry_min <= ny <= ry_max):
                continue

            # Connector sits between this room and its neighbor in grid-space
            if dx == 1  and 0 <= cx + 1 < gw: grid[cy][cx + 1]     = "-"
            elif dx == -1 and 0 <= cx - 1 < gw: grid[cy][cx - 1]   = "-"
            elif dy == 1  and 0 <= cy - 1 < gh: grid[cy - 1][cx]   = "|"
            elif dy == -1 and 0 <= cy + 1 < gh: grid[cy + 1][cx]   = "|"

    return "\n".join("".join(row) for row in grid)
