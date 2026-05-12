"""
Starter-tier garments issued by OASMC at academy intake. Cloth, minimal
flat mitigation — meant to fill slots, not protect.
"""

SCUFFED_BOOTS = {
    "prototype_key": "scuffed_boots",
    "prototype_parent": ("tier_starter", "armor_base"),
    "prototype_desc": "OASMC-issue starter boots.",
    "prototype_tags": ["starter", "armor", "oasmc"],
    "key": "scuffed boots",
    "aliases": ["boots"],
    "desc": (
        "A pair of leather boots scuffed nearly grey from years of academy "
        "use. The soles are honest, if thin, and the laces have been "
        "replaced more than once."
    ),
    "tags": [
        ("feet", "slot"),
        ("cloth", "material"),
    ],
    "attrs": [
        ("armor_value", 1),
    ],
}

PATCHED_TROUSERS = {
    "prototype_key": "patched_trousers",
    "prototype_parent": ("tier_starter", "armor_base"),
    "prototype_desc": "OASMC-issue starter trousers.",
    "prototype_tags": ["starter", "armor", "oasmc"],
    "key": "patched trousers",
    "aliases": ["trousers", "pants"],
    "desc": (
        "Sturdy canvas trousers, patched at the knees and seat by an "
        "indifferent quartermaster. They fit well enough and don't "
        "advertise where you've been."
    ),
    "tags": [
        ("legs", "slot"),
        ("cloth", "material"),
    ],
    "attrs": [
        ("armor_value", 1),
    ],
}

HOMESPUN_SHIRT = {
    "prototype_key": "homespun_shirt",
    "prototype_parent": ("tier_starter", "armor_base"),
    "prototype_desc": "OASMC-issue starter shirt.",
    "prototype_tags": ["starter", "armor", "oasmc"],
    "key": "homespun shirt",
    "aliases": ["shirt"],
    "desc": (
        "An undyed homespun shirt, soft from washing and faintly smelling "
        "of cedar from the academy linen room. The collar has been "
        "re-stitched at least twice."
    ),
    "tags": [
        ("chest", "slot"),
        ("cloth", "material"),
    ],
    "attrs": [
        ("armor_value", 1),
    ],
}
