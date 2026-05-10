"""
OASMC onboarding items issued at academy intake. Some are character-bound.
"""

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
    "locks": "drop:false();give:false()",
    "tags": [("intake_token", "oasmc")],
}
