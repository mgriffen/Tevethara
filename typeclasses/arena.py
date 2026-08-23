"""
Practical Assessment Annex fixtures.

The annex is a stage built ahead of the combat engine: dummies carry the
stat attributes Combat Core will read (`hp_max`, `armor_value`, `evasion`,
`magic_resist`, `resists`) and nothing consumes them yet. The behavior in
this module is examine-only.
"""

from evennia.utils.utils import compress_whitespace

from typeclasses.objects import Object


def _examine_pass(obj, looker):
    """
    Count how many times `looker` has examined `obj`, 1-based.

    Stored per-looker on the object so two candidates on the same floor
    don't share a reading. Reassigned rather than mutated in place so the
    Attribute actually saves.
    """
    if not looker:
        return 1
    counts = dict(obj.db.examine_counts or {})
    key = str(looker.id)
    counts[key] = counts.get(key, 0) + 1
    obj.db.examine_counts = counts
    return counts[key]


class ArenaFixture(Object):
    """Immobile annex fixture — signage, racks, instrumentation."""

    def at_object_creation(self):
        super().at_object_creation()
        self.locks.add("get:false();drop:false()")

    def format_appearance(self, appearance, looker, **kwargs):
        """
        Keep paragraph breaks. The default collapses runs of newlines to one,
        which runs the ledgers, forms and files here together into a block.
        """
        return compress_whitespace(appearance, max_linebreaks=2).strip()


class TrainingDummy(ArenaFixture):
    """
    An assessment post. Carries the attributes Combat Core will read; the
    typeclass itself only appends the asset plate to the description.
    """

    def get_display_desc(self, looker, **kwargs):
        desc = super().get_display_desc(looker, **kwargs)
        tag = self.db.asset_tag
        if tag:
            desc = f"{desc}\n\nA brass plate at the base reads |y{tag}|n."
        return desc


class Bartholomew(TrainingDummy):
    """
    Asset OASMC-0001. Repeated examination drains rather than builds — each
    pass takes something away from the reading before it, and the last one
    stands.
    """

    _PASSES = [
        (
            "An assessment post, older than the ones beside it and made "
            "differently — cut and shaped by hand rather than turned. The "
            "straw is fresh. The binding is new. The facing boards are recent "
            "enough that the grain still shows pale where the plane took it."
        ),
        (
            "Every part of it is newer than the posts beside it, and those "
            "have stood here since the annex was extended. The straw is "
            "replaced on schedule, the binding when it frays, the boards when "
            "they split.\n"
            "\n"
            "The wear is not where you would expect. The facing is scarred at "
            "chest height like the others. It is also worn smooth at the base, "
            "in a band a hand wide, all the way round."
        ),
        (
            "The core of the post is not academy timber. It is a darker wood, "
            "close-grained, and the joins are cut in a way the annex's own "
            "carpenters do not use — visible where the facing board has pulled "
            "a little away from the shoulder.\n"
            "\n"
            "There is no lathe mark anywhere on it. There is no maker's stamp."
        ),
        (
            "It has stood on this floor taking everything the Academy has ever "
            "taught anyone to do, since before the Academy was here. The straw "
            "is new. The binding is new. The boards are new.\n"
            "\n"
            "Nobody has measured the post.\n"
            "\n"
            "The file in the Records Office runs to forty-one years and does "
            "not describe it once. It only argues about what it is worth."
        ),
    ]

    def get_display_desc(self, looker, **kwargs):
        pass_no = _examine_pass(self, looker)
        desc = self._PASSES[min(pass_no, len(self._PASSES)) - 1]
        tag = self.db.asset_tag
        if tag:
            desc = f"{desc}\n\nA brass plate at the base reads |y{tag}|n."
        return desc


class WardHairline(ArenaFixture):
    """
    The crack in the Evocation Cell ward-line. Nothing in the annex accounts
    for it and the Office has closed the file on it three times.
    """

    _FIRST = (
        "The ward-line runs unbroken around the cell — that is the whole point "
        "of it. At one place, low on the north wall, there is a crack.\n"
        "\n"
        "It is too fine to be damage. It does not cross the channel; it runs "
        "along it, inside the alloy, the length of two hands.\n"
        "\n"
        "When you look at it directly, something in it |mpulses|n.\n"
        "\n"
        "|mPink|n. |mPurple|n.\n"
        "The colour has no name in the language you use for colours.\n"
        "\n"
        "It beats once, slowly, and stops. The wall is grey again."
    )

    _AFTER = (
        "The crack has not changed. Nothing in this room has changed.\n"
        "\n"
        "It pulses when you look at it, and stops when you stop.\n"
        "\n"
        "|mNot toward you specifically.|n\n"
        "\n"
        "|xJust — toward.|n"
    )

    def get_display_desc(self, looker, **kwargs):
        return self._FIRST if _examine_pass(self, looker) == 1 else self._AFTER


class SuggestionBox(ArenaFixture):
    """
    Records Office suggestion box. Locked, unemptied, and holding exactly one
    thing. It stays inside the box.
    """

    _FIRST = (
        "A wooden box with a slot in the lid, screwed to the wall. The slot is "
        "furred with dust. The lock is a simple one and the key is not on the "
        "ring at the desk.\n"
        "\n"
        "Through the slot, one folded paper is visible. It has been in there "
        "long enough to have taken the shape of the box."
    )

    _AFTER = (
        "Tilting your head to the slot, one line of it is readable where the "
        "fold turns:\n"
        "\n"
        '  |x"— and I have raised it four times and been told each time that '
        'the —"|n\n'
        "\n"
        "The rest is inside the box."
    )

    def get_display_desc(self, looker, **kwargs):
        return self._FIRST if _examine_pass(self, looker) == 1 else self._AFTER
