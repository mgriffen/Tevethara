"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def at_object_creation(self):
        """Called once when the character is first created."""
        super().at_object_creation()
        # OASMC Intake tracking
        self.db.race = None
        self.db.char_class = None
        self.db.intake_step = 0   # tracks progress through onboarding
        self.db.intake_complete = False
        # Intro cutscene tracking
        self.db.intro_seen = False

    def at_post_puppet(self, **kwargs):
        if not self.db.intro_seen:
            self._run_intro_cutscene()
        else:
            super().at_post_puppet(**kwargs)

    def _run_intro_cutscene(self):
        from evennia.utils.utils import delay
        from evennia.utils.search import search_object
        ferry = search_object("Ferry Passenger Hold")
        if ferry:
            self.move_to(ferry[0], quiet=True, move_type="teleport")
        self._intro_beat_0()
        delay(4,  self._intro_beat_1)
        delay(10, self._intro_beat_2)
        delay(17, self._intro_beat_3)
        delay(23, self._intro_beat_4)
        delay(28, self._intro_beat_5)
        delay(32, self._intro_beat_6)

    def _intro_beat_0(self):
        self.msg(
            "\n\n"
            "|xThe island has been growing for an hour.|n\n\n"
            "You can see it clearly now from the stern rail — low grey cliffs, "
            "a smear of buildings above the waterline, the OASMC complex asserting "
            "itself against the sky with the confidence of something built by committee "
            "and paid for by someone else.\n\n"
            "The ferry |wrocks|n. Salt air. Tar. The creak of a hull that has made "
            "this crossing more times than anyone has bothered to count.\n\n"
            "You meant to stay awake for the approach.\n\n"
            "|xYour eyes grow heavy.|n"
        )

    def _intro_beat_1(self):
        self.msg(
            "\n"
            "|xThe sky is wrong.|n\n\n"
            "Not dark — |mdark|n. The difference is felt before it is understood.\n\n"
            "Across the horizon: a streak of fire. Not lightning. Not a signal flare. "
            "Something |wlarger|n, moving with the patient certainty of things "
            "that do not know they should stop."
        )

    def _intro_beat_2(self):
        self.msg(
            "\n"
            "|rThe horizon fills.|n\n\n"
            "Sound arrives a moment after the light — the kind that is not heard "
            "so much as |rfelt|n, deep in the chest, behind the teeth.\n\n"
            "Stone and water, |rscreaming|n.\n\n"
            "The world |rsplits|n."
        )

    def _intro_beat_3(self):
        self.msg(
            "\n"
            "|xSilence.|n\n\n"
            "Then: deep underground — far enough that the concept of 'down' "
            "has become abstract — something |mpulses|n.\n\n"
            "|mPink|n. |mPurple|n. The color has no name in the language "
            "you use for colors.\n\n"
            "It beats like a second heart. Slower than yours. Older.\n\n"
            "|xIt does not know what it is. It only knows that it |mis|n|x.|n"
        )

    def _intro_beat_4(self):
        self.msg(
            "\n"
            "It knows you are here.\n\n"
            "Not a thought. Not a signal. A |mrecognition|n — "
            "the way a lodestone turns, the way still water knows "
            "the shape of what disturbs it.\n\n"
            "Something reaches.\n\n"
            "|mNot toward you specifically.|n\n\n"
            "|xJust — toward.|n"
        )

    def _intro_beat_5(self):
        self.msg(
            "\n"
            "|wYou wake.|n\n\n"
            "Hull-thump. The particular sound of a ferry meeting a pier "
            "at a speed that someone in an office has decided is acceptable.\n\n"
            "Salt air. The shriek of gulls.\n\n"
            "Around you, the other passengers are already on their feet — "
            "gathering bags, moving for the gangplank with the coordinated "
            "shuffle of people who have been sitting for two hours and "
            "are not going to be last off the boat.\n\n"
            "|xAnuvara Bay. The OASMC island. You have arrived.|n"
        )

    def _intro_beat_6(self):
        self.db.intro_seen = True
        if self.location:
            self.msg(
                (self.at_look(self.location), {"type": "look"}), options=None
            )
            def _announce(obj, from_obj):
                obj.msg(
                    f"{self.get_display_name(obj)} has entered the game.",
                    from_obj=from_obj,
                )
            self.location.for_contents(_announce, exclude=[self], from_obj=self)
