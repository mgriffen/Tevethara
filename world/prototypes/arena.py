"""
Practical Assessment Annex fixtures — assessment posts, signage, racks and
instrumentation.

The posts carry the stat attributes Combat Core will read. Each variant moves
exactly one axis off the DUMMY_BASE baseline, so when the engine lands a bad
number has one possible source.

Asset tags: the milled posts are OASMC-4471 through -4478. OASMC-0001 is not
milled and is not from that series.
"""

# ---------------------------------------------------------------------------
# Assessment posts
# ---------------------------------------------------------------------------

_POST_DESC = (
    "A turned post on a squared base, wrapped in straw and bound with cord, "
    "faced with board at chest height. Milled, numbered, and identical to "
    "every other post in the annex."
)

DUMMY_FLOOR_PLAIN = {
    "prototype_key": "dummy_floor_plain",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4471 — unmodified baseline.",
    "prototype_tags": ["arena", "dummy"],
    "key": "assessment post",
    "aliases": ["post", "dummy", "4471"],
    "desc": _POST_DESC,
    "attrs": [
        ("asset_tag", "OASMC-4471"),
    ],
}

DUMMY_FLOOR_ARMORED = {
    "prototype_key": "dummy_floor_armored",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4472 — varies armor_value only.",
    "prototype_tags": ["arena", "dummy"],
    "key": "banded assessment post",
    "aliases": ["banded post", "banded", "4472"],
    "desc": (
        _POST_DESC + "\n"
        "\n"
        "A banded plate has been strapped over the facing boards — the same "
        "pattern the Office issues, worn through in the same places."
    ),
    "attrs": [
        ("asset_tag", "OASMC-4472"),
        ("armor_value", 12),
    ],
}

DUMMY_RANGE_STATIC = {
    "prototype_key": "dummy_range_static",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4473 — range baseline, fixed.",
    "prototype_tags": ["arena", "dummy"],
    "key": "range post",
    "aliases": ["range", "4473"],
    "desc": (
        _POST_DESC + "\n"
        "\n"
        "It stands on the twenty, bolted down, and has stood on the twenty "
        "for as long as the painted numerals have been there."
    ),
    "attrs": [
        ("asset_tag", "OASMC-4473"),
    ],
}

DUMMY_RANGE_SWINGING = {
    "prototype_key": "dummy_range_swinging",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4474 — varies evasion only.",
    "prototype_tags": ["arena", "dummy"],
    "key": "swinging post",
    "aliases": ["swinging", "pivot post", "4474"],
    "desc": (
        _POST_DESC + "\n"
        "\n"
        "This one is set on a pivot mount rather than a fixed base. A pull-cord "
        "runs from it back to the firing line, so an instructor can set it "
        "moving before a candidate looses."
    ),
    "attrs": [
        ("asset_tag", "OASMC-4474"),
        ("evasion", 25),
    ],
}

DUMMY_TECHNIQUE = {
    "prototype_key": "dummy_technique",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4475 — varies hp_max only; outlasts a rotation.",
    "prototype_tags": ["arena", "dummy"],
    "key": "braced assessment post",
    "aliases": ["braced post", "braced", "4475"],
    "desc": (
        _POST_DESC + "\n"
        "\n"
        "This one is strapped into the floor with four iron bands rather than "
        "bolted to a base plate. It is not meant to move at all, and it does "
        "not."
    ),
    "attrs": [
        ("asset_tag", "OASMC-4475"),
        ("hp_max", 2000),
    ],
}

# The pit posts are deliberately identical to one another — the threat table
# is what is being read there, so the targets must not differ.
_PIT_DESC = (
    _POST_DESC + "\n"
    "\n"
    "It stands close enough to the next post that a candidate cannot face "
    "both."
)

DUMMY_PIT_A = {
    "prototype_key": "dummy_pit_a",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Assessment post 4476 — pit baseline, one of three identical.",
    "prototype_tags": ["arena", "dummy"],
    "key": "pit post",
    "aliases": ["post", "4476"],
    "desc": _PIT_DESC,
    "attrs": [
        ("asset_tag", "OASMC-4476"),
    ],
}

DUMMY_PIT_B = dict(
    DUMMY_PIT_A,
    prototype_key="dummy_pit_b",
    prototype_desc="Assessment post 4477 — pit baseline, one of three identical.",
    aliases=["post", "4477"],
    attrs=[("asset_tag", "OASMC-4477")],
)

DUMMY_PIT_C = dict(
    DUMMY_PIT_A,
    prototype_key="dummy_pit_c",
    prototype_desc="Assessment post 4478 — pit baseline, one of three identical.",
    aliases=["post", "4478"],
    attrs=[("asset_tag", "OASMC-4478")],
)

WARD_TARGET = {
    "prototype_key": "ward_target",
    "prototype_parent": ("dummy_base",),
    "prototype_desc": "Evocation Cell target — varies magic_resist only.",
    "prototype_tags": ["arena", "dummy"],
    "key": "warded target post",
    "aliases": ["target post", "target", "warded post"],
    "desc": (
        "A post of the same grey alloy as the ward-lines, set into the floor at "
        "the focus of the cell, the channels running up it and closing at the "
        "cap. It does not take a polish either.\n"
        "\n"
        "Cast at it and the cell reads what lands. That is the whole of its "
        "purpose. It is not built to be struck."
    ),
    "attrs": [
        ("asset_tag", "OASMC-W-12"),
        ("magic_resist", 25),
    ],
}

BARTHOLOMEW = {
    "prototype_key": "bartholomew",
    "prototype_parent": ("dummy_base",),
    "typeclass": "typeclasses.arena.Bartholomew",
    "prototype_desc": "Asset OASMC-0001. Not milled, not from the 4471 series.",
    "prototype_tags": ["arena", "dummy"],
    "key": "hand-cut assessment post",
    "aliases": ["hand-cut post", "old post", "0001"],
    "desc": "",  # supplied per-examination by the typeclass
    "attrs": [
        ("asset_tag", "OASMC-0001"),
    ],
}

# ---------------------------------------------------------------------------
# Signage, racks, instrumentation
# ---------------------------------------------------------------------------

_FIXTURE = "typeclasses.arena.ArenaFixture"

ANNEX_WAIVER = {
    "prototype_key": "annex_waiver",
    "typeclass": _FIXTURE,
    "prototype_desc": "The waiver form in the Annex Vestibule tray.",
    "prototype_tags": ["arena", "signage"],
    "key": "assessment waiver",
    "aliases": ["waiver", "form", "forms"],
    "desc": (
        "A printed form, four sides, most of it in a smaller type than the "
        "first side. The candidate's part runs to nine lines. The countersigning "
        "instructor's part is one.\n"
        "\n"
        "  |ySECTION 1 — CANDIDATE. I have read the Practicum Standards and "
        "understand that assessment is conducted under conditions selected to "
        "be adverse.|n\n"
        "  |ySECTION 4 — NEXT OF KIN OR NOMINATED CORRESPONDENT.|n\n"
        "\n"
        "The tray beneath holds a stack of these, completed and countersigned, "
        "that nobody has collected."
    ),
}

ANNEX_SIGNIN_LEDGER = {
    "prototype_key": "annex_signin_ledger",
    "typeclass": _FIXTURE,
    "prototype_desc": "The sign-in ledger on the vestibule desk.",
    "prototype_tags": ["arena", "signage"],
    "key": "sign-in ledger",
    "aliases": ["ledger", "sign-in", "signin"],
    "desc": (
        "Open to today. Name, discipline, instructor, time down, time up. The "
        "last column is filled in by whoever is at the desk when a candidate "
        "comes back up the stair.\n"
        "\n"
        "The desk is unstaffed. Four names on this page have a time down and no "
        "time up, and the pen is where it was left."
    ),
}

REQUISITION_LEDGER = {
    "prototype_key": "requisition_ledger",
    "typeclass": _FIXTURE,
    "prototype_desc": "The requisition ledger, chained to the counter.",
    "prototype_tags": ["arena", "signage"],
    "key": "requisition ledger",
    "aliases": ["ledger", "requisition"],
    "desc": (
        "A bound ledger, chained to the counter, open to the current quarter. "
        "Issues on the left, returns on the right. The returns column is "
        "shorter.\n"
        "\n"
        "Near the foot of the standing-items page, in a hand that has plainly "
        "resented writing it for years:\n"
        "\n"
        "  |yCONSUMABLE — BACKSTOP, EARTHEN. REPLACED. See previous. See "
        "previous.|n"
    ),
}

PRACTICE_RACK = {
    "prototype_key": "practice_rack",
    "typeclass": _FIXTURE,
    "prototype_desc": "Floor rack of blunted practice weapons.",
    "prototype_tags": ["arena", "fixture"],
    "key": "practice rack",
    "aliases": ["rack", "weapons"],
    "desc": (
        "Blunted practice weapons in a floor rack, sorted by weight rather than "
        "by type, so a hand-axe stands between two shortswords. Every haft "
        "carries a burned-in number.\n"
        "\n"
        "Three of the numbers have no matching line in the ledger, and have not "
        "had one for some time."
    ),
}

DEPRECIATION_FILE = {
    "prototype_key": "depreciation_file",
    "typeclass": _FIXTURE,
    "prototype_desc": "The standing depreciation query on asset OASMC-0001.",
    "prototype_tags": ["arena", "signage", "easter_egg"],
    "key": "standing query",
    "aliases": ["query", "file", "depreciation"],
    "desc": (
        "|yANNEX FIXTURE DEPRECIATION — STANDING QUERY|n\n"
        "|yRe: asset OASMC-0001, assessment post, Practical Assessment Floor.|n\n"
        "\n"
        "The post has been in continuous service since before the current "
        "numbering scheme was adopted, which is why it carries the number it "
        "carries. Its straw has been replaced on schedule. Its binding has been "
        "replaced. Its facing boards have been replaced twice within living "
        "memory, and the base plate was recut in a year the file does not give.\n"
        "\n"
        "Compliance holds that an asset which has had every component replaced "
        "is a new asset and must be re-registered at current value. The Annex "
        "holds that the asset has never been out of service, that no "
        "re-registration was ever raised, and that the post is therefore the "
        "same post.\n"
        "\n"
        "The query has been open for forty-one years. It is reviewed annually. "
        "Neither position has moved.\n"
        "\n"
        "No party to the query has proposed replacing the post."
    ),
}

SUGGESTION_BOX = {
    "prototype_key": "suggestion_box",
    "typeclass": "typeclasses.arena.SuggestionBox",
    "prototype_desc": "Records Office suggestion box. Locked, unemptied.",
    "prototype_tags": ["arena", "fixture", "easter_egg"],
    "key": "suggestion box",
    "aliases": ["box", "suggestions"],
    "desc": "",  # supplied per-examination by the typeclass
}

RANGE_BACKSTOP = {
    "prototype_key": "range_backstop",
    "typeclass": _FIXTURE,
    "prototype_desc": "The earthen backstop at the end of the discharge gallery.",
    "prototype_tags": ["arena", "fixture"],
    "key": "earthen backstop",
    "aliases": ["backstop", "earth", "mat"],
    "desc": (
        "Packed earth faced with hanging rope mat, filling the whole of the far "
        "end. The mat is new in the centre and old at the edges.\n"
        "\n"
        "Behind it the earth has been dug out and replaced often enough that "
        "the gallery floor sits two inches lower at that end than at the firing "
        "line."
    ),
}

ANNEX_PLAN = {
    "prototype_key": "annex_plan",
    "typeclass": _FIXTURE,
    "prototype_desc": "Painted plan of the annex, mounted in the Cadence Corridor.",
    "prototype_tags": ["arena", "signage"],
    "key": "plan of the annex",
    "aliases": ["plan", "map board", "board"],
    "desc": (
        "Painted on a board and varnished over: eleven rooms and the stair. It "
        "is accurate, and it is the only plan in the building.\n"
        "\n"
        "Someone has scratched an arrow into the varnish beside this corridor's "
        "own room, pointing at the door to the conditions suite, and then "
        "scratched it out again."
    ),
}

WARD_SURVEY_PLATES = {
    "prototype_key": "ward_survey_plates",
    "typeclass": _FIXTURE,
    "prototype_desc": "Three survey plates beside the hairline in the ward-line.",
    "prototype_tags": ["arena", "signage"],
    "key": "survey plates",
    "aliases": ["plates", "plate", "survey"],
    "desc": (
        "Three small plates screwed to the wall, one above the other. The "
        "uppermost is the newest:\n"
        "\n"
        "  |ySURVEYED UNDER §29/4. NO FAULT FOUND. FILE CLOSED.|n\n"
        "\n"
        "The two beneath it carry the same wording and different dates. The "
        "lowest has been there long enough that the screws have bled rust into "
        "the stone."
    ),
}

WARD_HAIRLINE = {
    "prototype_key": "ward_hairline",
    "typeclass": "typeclasses.arena.WardHairline",
    "prototype_desc": "The crack in the Evocation Cell ward-line.",
    "prototype_tags": ["arena", "fixture", "easter_egg"],
    "key": "hairline",
    "aliases": ["crack", "ward-line", "ward line", "line"],
    "desc": "",  # supplied per-examination by the typeclass
}

CONDITION_KIT = {
    "prototype_key": "condition_kit",
    "typeclass": _FIXTURE,
    "prototype_desc": "The equipment laid out on the bench in the conditions suite.",
    "prototype_tags": ["arena", "fixture"],
    "key": "equipment on the bench",
    "aliases": ["equipment", "bench", "kit"],
    "desc": (
        "Laid out in the order it is used: a folded blindfold, laundered. A "
        "silencing collar, sized. Two padded cuffs on a short chain. A wooden "
        "haft, for taking out of the candidate's hands.\n"
        "\n"
        "Beside them, a slate with the schedule on it. The schedule is by name, "
        "and it has a column for the second time."
    ),
}

ASSESSMENT_SLATE = {
    "prototype_key": "assessment_slate",
    "typeclass": _FIXTURE,
    "prototype_desc": "The instructor's recording slate in the Observation Gallery.",
    "prototype_tags": ["arena", "fixture"],
    "key": "assessment slate",
    "aliases": ["slate", "slates"],
    "desc": (
        "Ruled into columns — candidate, fixture, elapsed, outcome — written up "
        "by hand during an assessment, copied into the Records Office "
        "afterward, and wiped.\n"
        "\n"
        "The chalk ghost of the last entry is still legible if you stand at the "
        "right angle to the lamp:\n"
        "\n"
        "  |x…    …    0:00:11    …|n\n"
        "\n"
        "The outcome column is the only one that has been wiped twice."
    ),
}
