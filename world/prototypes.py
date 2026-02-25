"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.
"""

# ---------------------------------------------------------------------------
# OASMC Onboarding Item
# ---------------------------------------------------------------------------

ACADEMY_INTAKE_TOKEN = {
    "prototype_key": "ACADEMY_INTAKE_TOKEN",
    "key": "Academy Intake Token",
    "typeclass": "typeclasses.objects.Object",
    "desc": (
        "A small warded disc of pale grey stone, no larger than a coin purse. "
        "The surface is etched with your name, lineage, and discipline in fine "
        "silver script, sealed beneath a faint amber glow. A Compliance stamp "
        "on the reverse reads: |yANUVARA OASMC – INTAKE CERTIFIED|n. "
        "It hums faintly when held near the Neutral Corridor checkpoint."
    ),
    # Cannot be dropped or given away — it's a character-bound pass
    "locks": "drop:false();give:false()",
    "tags": [("intake_token", "oasmc")],
}
