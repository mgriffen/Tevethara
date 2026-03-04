"""
One-time script to tag all existing rooms with map coordinates.
Run from the project root with:  evennia run world.apply_map_coords

Coordinate convention:  east = +x, west = -x, north = +y, south = -y
"""

import django
django.setup()

from evennia.utils.search import search_object

COORDS = {
    # area, room name, x, y
    # --- Ferry ---
    "Ferry Passenger Hold":       ("ferry",          0,   0),
    "Ferry Upper Deck":           ("ferry",          0,   1),
    # --- OASMC: compliance dock ---
    "Arrival Pier":               ("oasmc",          0,  10),
    "Pierside Queue":             ("oasmc",          0,   9),
    "Manifest Hall":              ("oasmc",          0,   8),
    "Intake Counter":             ("oasmc",         -1,   8),
    "Inspection Yard":            ("oasmc",          1,   8),
    "Harbor Notices Board":       ("oasmc",          2,   8),
    "Fee and Berth Office":       ("oasmc",          1,   7),
    # --- OASMC: character creation spine ---
    "Name Registry":              ("oasmc",          0,   6),
    "Identity Gallery":           ("oasmc",          0,   5),
    "Aptitude Annex":             ("oasmc",          0,   4),
    "Oath and Stamp Station":     ("oasmc",          0,   3),
    # --- OASMC: neutral corridor ---
    "Neutral Corridor Checkpoint":("oasmc",          0,   2),
    "Beacon Engine Vault":        ("oasmc",         -1,   2),
    "Neutral Corridor":           ("oasmc",          0,   1),
    # --- OASMC: academy campus ---
    "Student Gate Arch":          ("oasmc",          0,   0),
    "First Courtyard":            ("oasmc",          0,  -1),
    "Sanction Hall":              ("oasmc",          1,  -1),
    "Refectory Entrance":         ("oasmc",         -1,  -1),
    "Dormitory Gallery":          ("oasmc",          0,  -2),
    "Dorm Common Room":           ("oasmc",          1,  -2),
    # --- Sealed/restricted: own areas so they appear as ^ or v on parent ---
    "Understructure Stair":       ("understructure", 0,   0),
    "Faculty Tower Stair":        ("faculty_tower",  0,   0),
}


def run():
    ok = 0
    missing = []
    for room_name, (area, x, y) in COORDS.items():
        results = search_object(room_name, typeclass="typeclasses.rooms.Room")
        if not results:
            results = search_object(room_name)
        if not results:
            missing.append(room_name)
            continue
        room = results[0]
        room.db.map_area = area
        room.db.map_x = x
        room.db.map_y = y
        print(f"  Tagged: [{room.key}] area={area} x={x} y={y}")
        ok += 1

    print(f"\nDone: {ok} rooms tagged.")
    if missing:
        print(f"Not found ({len(missing)}): {', '.join(missing)}")


if __name__ == "__main__":
    run()
