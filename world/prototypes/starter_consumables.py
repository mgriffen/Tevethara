"""
Starter-tier consumables issued by OASMC at academy intake.
"""

BANDAGE = {
    "prototype_key": "bandage",
    "prototype_parent": ("tier_starter", "consumable_base"),
    "typeclass": "typeclasses.items.Bandage",
    "prototype_desc": "Field bandage — single use, takes time, blocked in combat.",
    "prototype_tags": ["starter", "consumable", "oasmc"],
    "key": "bandage",
    "aliases": ["bandages"],
    "desc": (
        "A neatly rolled strip of clean linen, sealed with a small wax "
        "stamp from the academy infirmary. Useful for closing minor wounds "
        "when there's a moment to breathe."
    ),
    "tags": [
        ("healing", "consumable_type"),
    ],
    "attrs": [
        ("value", 1),
    ],
}
