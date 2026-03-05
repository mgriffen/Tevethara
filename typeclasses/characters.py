"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


# ---------------------------------------------------------------------------
# Intro cutscene beat texts — broken into short lines for typewriter reveal
# ---------------------------------------------------------------------------

_BEAT_0 = (
    "\n\n"
    "|xThe island has been growing for an hour.|n\n"
    "\n"
    "You can see it clearly now from the stern rail —\n"
    "low grey cliffs,\n"
    "a smear of buildings above the waterline,\n"
    "the OASMC complex asserting itself against the sky\n"
    "with the confidence of something built by committee\n"
    "and paid for by someone else.\n"
    "\n"
    "The ferry |wrocks|n.\n"
    "Salt air. Tar.\n"
    "The creak of a hull that has made this crossing\n"
    "more times than anyone has bothered to count.\n"
    "\n"
    "You meant to stay awake for the approach.\n"
    "\n"
    "|xYour eyes grow heavy.|n"
)

_BEAT_1 = (
    "\n"
    "|xThe sky is wrong.|n\n"
    "\n"
    "Not dark — |mdark|n.\n"
    "The difference is felt before it is understood.\n"
    "\n"
    "Across the horizon: a streak of fire.\n"
    "Not lightning. Not a signal flare.\n"
    "Something |wlarger|n,\n"
    "moving with the patient certainty of things\n"
    "that do not know they should stop."
)

_BEAT_2 = (
    "\n"
    "|rThe horizon fills.|n\n"
    "\n"
    "Sound arrives a moment after the light —\n"
    "the kind that is not heard so much as |rfelt|n,\n"
    "deep in the chest, behind the teeth.\n"
    "\n"
    "Stone and water, |rscreaming|n.\n"
    "\n"
    "The world |rsplits|n."
)

_BEAT_3 = (
    "\n"
    "|xSilence.|n\n"
    "\n"
    "Then: deep underground —\n"
    "far enough that the concept of 'down'\n"
    "has become abstract —\n"
    "something |mpulses|n.\n"
    "\n"
    "|mPink|n. |mPurple|n.\n"
    "The color has no name in the language you use for colors.\n"
    "\n"
    "It beats like a second heart.\n"
    "Slower than yours. Older.\n"
    "\n"
    "|xIt does not know what it is.|n\n"
    "|xIt only knows that it |mis|n|x.|n"
)

_BEAT_4 = (
    "\n"
    "It knows you are here.\n"
    "\n"
    "Not a thought. Not a signal.\n"
    "A |mrecognition|n —\n"
    "the way a lodestone turns,\n"
    "the way still water knows\n"
    "the shape of what disturbs it.\n"
    "\n"
    "Something reaches.\n"
    "\n"
    "|mNot toward you specifically.|n\n"
    "\n"
    "|xJust — toward.|n"
)

_BEAT_5 = (
    "\n"
    "|wYou wake.|n\n"
    "\n"
    "Hull-thump.\n"
    "The particular sound of a ferry meeting a pier\n"
    "at a speed that someone in an office\n"
    "has decided is acceptable.\n"
    "\n"
    "Salt air. The shriek of gulls.\n"
    "\n"
    "Around you, the other passengers are already on their feet —\n"
    "gathering bags, moving for the gangplank\n"
    "with the coordinated shuffle of people\n"
    "who have been sitting for two hours\n"
    "and are not going to be last off the boat.\n"
    "\n"
    "|xAnuvara Bay. The OASMC island.|n\n"
    "|xYou have arrived.|n"
)

# Pairs of (beat_text, pause_after_in_seconds)
_BEATS = [
    (_BEAT_0, 12),
    (_BEAT_1, 14),
    (_BEAT_2, 10),
    (_BEAT_3, 14),
    (_BEAT_4, 12),
    (_BEAT_5, 6),
]


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

    def get_prompt(self):
        """Return the ASCII text prompt string showing current vitals."""
        hp     = self.db.hp or 100
        hp_max = self.db.hp_max or 100
        st     = self.db.stamina or 100
        st_max = self.db.stamina_max or 100
        mp     = self.db.mp or 50
        mp_max = self.db.mp_max or 50
        return (
            f"|x<|n"
            f"|rHP:{hp}/{hp_max}|n  "
            f"|yST:{st}/{st_max}|n  "
            f"|cMP:{mp}/{mp_max}|n"
            f"|x>|n"
        )

    def update_prompt(self):
        """Push the current prompt to the client."""
        self.msg(prompt=self.get_prompt())

    def send_map(self):
        """Render and push the current area map to the client via OOB."""
        if not self.location:
            return
        from world.map_render import render_area_map
        map_str = render_area_map(self.location)
        self.msg(oob=[("tev_map", [], {"data": map_str})])

    def at_post_move(self, source_location, move_type="move", **kwargs):
        """Send updated map whenever the character moves."""
        super().at_post_move(source_location, move_type=move_type, **kwargs)
        self.send_map()

    def at_post_puppet(self, **kwargs):
        if not self.db.intro_seen:
            self._run_intro_cutscene()
        else:
            super().at_post_puppet(**kwargs)
        self.update_prompt()
        self.send_map()

    # ------------------------------------------------------------------
    # Intro cutscene
    # ------------------------------------------------------------------

    def _typewrite(self, text, char_speed=0.030, done_callback=None):
        """
        Display text one line at a time. Delay per line scales with line
        length at ~30ms/character to approximate a typewriter feel.
        If the character disconnects mid-scene, stops silently.
        """
        from evennia.utils.utils import delay

        lines = text.split('\n')

        def _send(idx):
            if not self.sessions.all():
                return
            if idx >= len(lines):
                if done_callback:
                    done_callback()
                return
            self.msg(lines[idx])
            content = lines[idx].strip()
            speed = 0.25 if not content else max(0.20, len(content) * char_speed)
            delay(speed, _send, idx + 1)

        _send(0)

    def _run_intro_cutscene(self):
        from evennia.utils.search import search_object
        from evennia.utils.utils import delay

        ferry = search_object("Ferry Passenger Hold")
        if ferry:
            self.move_to(ferry[0], quiet=True, move_type="teleport")

        def play(idx):
            if not self.sessions.all():
                return
            if idx >= len(_BEATS):
                self._intro_finish()
                return
            text, pause = _BEATS[idx]
            def after_text():
                delay(pause, play, idx + 1)
            self._typewrite(text, done_callback=after_text)

        play(0)

    def _intro_finish(self):
        self.db.intro_seen = True
        self.send_map()
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
