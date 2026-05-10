"""
Starter-tier weapons issued by OASMC at intake or recovered from the
training racks.
"""

RUSTY_CUTLASS = {
    "prototype_key": "rusty_cutlass",
    "prototype_parent": ("tier_starter", "weapon_base"),
    "prototype_desc": "OASMC training cutlass — pitted and dull.",
    "prototype_tags": ["starter", "weapon", "oasmc"],
    "key": "rusty cutlass",
    "aliases": ["cutlass", "sword"],
    "desc": (
        "A pitted cutlass left in the academy training racks. The blade is "
        "dulled from years of practice swings, but the balance is honest."
    ),
    "tags": [
        ("slashing", "damage_type"),
        ("main_hand", "slot"),
    ],
    "attrs": [
        ("damage_min", 4),
        ("damage_max", 7),
    ],
}
