"""
Ferry-specific prototypes: the boat attendant NPC, your traveling satchel
(static flavor in the cargo hold), and the letter someone slipped into it.
"""

LETTER_BODY = (
    "|wFolded once. The seal is plain wax, no insignia, broken when you "
    "opened the satchel.|n\n"
    "\n"
    "To whoever finds this —\n"
    "\n"
    "Apologies for the imposition. I needed to get this off the ferry, "
    "and you looked like you would not be searched.\n"
    "\n"
    "Please bring it, unopened (too late now), to |yQuartermaster Velnis|n "
    "at the OASMC mess hall. She is expecting it, though not from you.\n"
    "\n"
    "If anyone in grey-and-amber asks what you are carrying, tell them "
    "it is a personal letter. It is, in fact, what it is.\n"
    "\n"
    "— A passenger who has already disembarked."
)

FERRY_LETTER = {
    "prototype_key": "ferry_letter",
    "typeclass": "typeclasses.objects.Object",
    "key": "folded letter",
    "aliases": ["letter"],
    "desc": LETTER_BODY,
    "prototype_desc": "The letter someone slipped into your satchel.",
    "prototype_tags": ["ferry", "quest_hook"],
    "tags": [("ferry_letter", "quest")],
    "locks": "get:all();drop:all()",
}

TRAVELING_SATCHEL = {
    "prototype_key": "traveling_satchel",
    "typeclass": "typeclasses.objects.Object",
    "key": "traveling satchel",
    "aliases": ["satchel", "bag"],
    "desc": (
        "A worn leather satchel — your own, recognizably so. The flap is "
        "open and the contents have been disturbed. Whatever was packed at "
        "the top is gone; in its place, a folded letter rests against the "
        "lining."
    ),
    "prototype_desc": "Your traveling satchel — static flavor in the cargo hold.",
    "prototype_tags": ["ferry"],
    "locks": "get:false();drop:false()",
}

FERRY_ATTENDANT = {
    "prototype_key": "ferry_attendant",
    "typeclass": "typeclasses.npcs.BoatAttendant",
    "key": "ferry attendant",
    "aliases": ["attendant"],
    "desc": (
        "A wiry woman in a salt-stained coat, hair pinned back under a "
        "knitted cap. She has the patient expression of someone who has "
        "spent twenty years rousing sleeping passengers and isn't tired "
        "of it yet."
    ),
    "prototype_desc": "The ferry attendant in the Passenger Hold.",
    "prototype_tags": ["ferry"],
    "locks": "get:false();drop:false()",
}
