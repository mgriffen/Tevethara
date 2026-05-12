"""
Abstract prototype parents. Not meant to be spawned directly — they
provide shared attrs/tags for concrete child prototypes.

Tuning a tier (e.g., starter durability) is one edit here followed by
batch_update_objects_with_prototype("tier_starter", exact=False).

Convention: in prototype_parent tuples, list rarity/tier parents FIRST
and the kind-defining parent (weapon_base, armor_base, ...) LAST.
Evennia auto-injects a default typeclass on every module-level
prototype, and parents merge left-to-right with later winning — so the
typeclass-bearing parent has to come last to actually take effect.
"""

WEAPON_BASE = {
    "prototype_key": "weapon_base",
    "typeclass": "typeclasses.items.Weapon",
    "prototype_desc": "Abstract weapon parent.",
    "prototype_tags": ["abstract", "weapon"],
    "tags": [("weapon", "category")],
    "attrs": [
        ("swing_time", 1.5),
        ("damage_min", 1),
        ("damage_max", 2),
        ("accuracy", 0),
        ("crit_bonus", 0),
        ("weight", 1.0),
    ],
    "locks": "get:all();drop:all()",
}

ARMOR_BASE = {
    "prototype_key": "armor_base",
    "typeclass": "typeclasses.items.Armor",
    "prototype_desc": "Abstract armor parent.",
    "prototype_tags": ["abstract", "armor"],
    "tags": [("armor", "category")],
    "attrs": [
        ("armor_value", 0),
        ("weight", 1.0),
    ],
    "locks": "get:all();drop:all()",
}

CONSUMABLE_BASE = {
    "prototype_key": "consumable_base",
    "typeclass": "typeclasses.items.Consumable",
    "prototype_desc": "Abstract consumable parent.",
    "prototype_tags": ["abstract", "consumable"],
    "tags": [("consumable", "category")],
    "attrs": [
        ("weight", 0.1),
    ],
    "locks": "get:all();drop:all()",
}

TIER_STARTER = {
    "prototype_key": "tier_starter",
    "prototype_desc": "Abstract starter-tier parent.",
    "prototype_tags": ["abstract", "tier"],
    "tags": [("starter", "rarity")],
    "attrs": [
        ("durability", 50),
        ("value", 3),
    ],
}
