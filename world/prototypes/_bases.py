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

DUMMY_BASE = {
    "prototype_key": "dummy_base",
    "typeclass": "typeclasses.arena.TrainingDummy",
    "prototype_desc": "Abstract training-dummy parent.",
    "prototype_tags": ["abstract", "dummy"],
    "tags": [("training_dummy", "category")],
    "attrs": [
        # Combat Core reads these. Nothing does yet — the engine is project B.
        ("hp_max", 200),
        ("armor_value", 0),
        ("evasion", 0),
        ("magic_resist", 0),
        # Per-type resists per Damage Types. Transcendent is deliberately
        # absent — it cannot be resisted.
        ("resists", {
            "crushing": 0, "piercing": 0, "slashing": 0, "unarmed": 0,
            "fire": 0, "frost": 0, "lightning": 0, "acid": 0, "poison": 0,
            "holy": 0, "unholy": 0, "celestium": 0,
        }),
        ("asset_tag", ""),
    ],
    "locks": "get:false();drop:false()",
}
