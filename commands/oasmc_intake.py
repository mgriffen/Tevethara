"""
commands/oasmc_intake.py

Diegetic character creation commands for the OASMC onboarding flow.
Each command is only meaningful in its designated intake room (enforced
by checking location.db.intake_step against REQUIRED_STEP).

Intake flow:
  Step 1 – Manifest Hall          → `begin intake`
  Step 2 – Name Registry          → `set name <name>`
  Step 3 – Identity Gallery       → `choose <race>`
  Step 4 – Aptitude Annex         → `choose <class>`
  Step 5 – Oath & Stamp Station   → `confirm` (or `reconsider`)

After confirmation the player receives an Academy Intake Token and is
directed toward the Neutral Corridor checkpoint.
"""

from evennia import Command, CmdSet
from evennia.prototypes.spawner import spawn

# ---------------------------------------------------------------------------
# Available choices
# ---------------------------------------------------------------------------

RACES = {
    "human": {
        "display": "Human",
        "desc": "Adaptable and numerous, found across all four continents.",
        "common_in": "Alda, Thalassia",
    },
    "elf": {
        "display": "Elf",
        "desc": "Long-lived and attuned to nature's rhythms. Three subraces known.",
        "common_in": "Forest reaches of Alda",
    },
    "half-elf": {
        "display": "Half-Elf",
        "desc": "Born between worlds, welcome in most — belonging in none.",
        "common_in": "Port cities, trade routes",
    },
    "dwarf": {
        "display": "Dwarf",
        "desc": "Stout, resilient, unmatched in craft and stubbornness.",
        "common_in": "Mountain holds of northern Alda",
    },
    "halfling": {
        "display": "Halfling",
        "desc": "Small in stature, sharp in wit, and suspiciously lucky.",
        "common_in": "Rural Alda, river settlements",
    },
}

CLASSES = {
    "warrior": {
        "display": "Warrior",
        "desc": "Masters of weapon and armor. The backbone of any front line.",
        "instructor": "Drill Yard",
    },
    "rogue": {
        "display": "Rogue",
        "desc": "Specialists in stealth, precision, and acts of questionable legality.",
        "instructor": "Practical Skills Hall",
    },
    "ranger": {
        "display": "Ranger",
        "desc": "Hunters and trackers, deadly at range and at home in the wild.",
        "instructor": "Archery Line",
    },
    "mage": {
        "display": "Mage",
        "desc": "Power through study and discipline. Arcane geometry, controlled channeling, lattice theory.",
        "instructor": "Arcane Lecture Hall",
    },
    "sorcerer": {
        "display": "Sorcerer",
        "desc": "Raw Celestium channeled through force of will. Powerful. Most who try this path do not survive it.",
        "instructor": "Arcane Lecture Hall",
    },
    "cleric": {
        "display": "Cleric",
        "desc": "Devoted servants of the divine, healers and warriors of faith.",
        "instructor": "Oath Chapel",
    },
    "paladin": {
        "display": "Paladin",
        "desc": "Oath-bound holy warriors. The oath is not optional.",
        "instructor": "Oath Chapel",
    },
    "druid": {
        "display": "Druid",
        "desc": "Guardians of natural order, shapers of living things.",
        "instructor": "Green Court Conservatory",
    },
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _in_intake_step(caller, required_step):
    """Return True if caller's location is the correct intake step."""
    loc = caller.location
    if not loc:
        return False
    return loc.db.intake_step == required_step


def _race_list():
    lines = ["|wAvailable lineages:|n"]
    for key, data in RACES.items():
        lines.append(f"  |y{data['display']:12s}|n — {data['desc']}")
        lines.append(f"               |x(Common in: {data['common_in']})|n")
    lines.append("\nType |wchoose <lineage>|n to select.")
    return "\n".join(lines)


def _class_list():
    lines = ["|wDiscipline Tablets on display:|n"]
    for key, data in CLASSES.items():
        lines.append(f"  |y{data['display']:12s}|n — {data['desc']}")
    lines.append("\nType |wchoose <discipline>|n to select.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Step 1 — Begin Intake (Manifest Hall)
# ---------------------------------------------------------------------------

class CmdBeginIntake(Command):
    """
    Begin the OASMC intake process.

    Usage:
      begin intake

    Only works in the Manifest Hall.
    """

    key = "begin intake"
    aliases = ["begin", "start intake"]
    help_category = "OASMC Intake"

    def func(self):
        if not _in_intake_step(self.caller, 1):
            self.caller.msg("There is nothing to begin here.")
            return

        if self.caller.db.intake_complete:
            self.caller.msg(
                "Your intake is already complete. Your token is in your inventory."
            )
            return

        self.caller.msg(
            "The Intake Clerk glances up from a stack of manifests and fixes you "
            "with the expression of someone who has done this ten thousand times.\n\n"
            '|yClerk:|n "Name. Origin. Aptitude. In that order. |wDon\'t improvise.|n"\n\n'
            "She jerks a thumb toward the side corridor.\n\n"
            '|yClerk:|n "Name Registry is through there. Move along."\n\n'
            "A door to the |wName Registry|n is now visible to the |wsouth|n."
        )
        # Unlock the exit to Name Registry
        name_registry = self.caller.search(
            "Name Registry", global_search=True, quiet=True
        )
        self.caller.db.intake_step = 2

        # Move caller into the Name Registry room if it exists
        exit_obj = self.caller.search("south", candidates=self.caller.location.exits, quiet=True)
        if exit_obj:
            self.caller.move_to(exit_obj[0].destination, quiet=True)
            self.caller.execute_cmd("look")
        else:
            self.caller.msg(
                "(The Name Registry exit isn't visible yet — ask a Warden for directions.)"
            )


# ---------------------------------------------------------------------------
# Step 2 — Set Name (Name Registry)
# ---------------------------------------------------------------------------

class CmdSetName(Command):
    """
    Register your name in the OASMC ledger.

    Usage:
      set name <your name>

    Only works in the Name Registry.
    """

    key = "set name"
    aliases = ["register name", "name"]
    help_category = "OASMC Intake"

    def func(self):
        if not _in_intake_step(self.caller, 2):
            self.caller.msg("There is no ledger here for you to sign.")
            return

        if not self.args.strip():
            self.caller.msg('Usage: |wset name <your name>|n\nExample: set name Aldric')
            return

        name = self.args.strip()

        # Basic name validation
        if len(name) < 2 or len(name) > 24:
            self.caller.msg(
                '|yClerk:|n "Names must be between 2 and 24 characters. '
                "Try again.\""
            )
            return
        if not name.replace("-", "").replace("'", "").isalpha():
            self.caller.msg(
                '|yClerk:|n "Letters only, please. Apostrophes and hyphens '
                "are acceptable. Numbers are not a name.\""
            )
            return

        display_name = name.capitalize()
        self.caller.key = display_name
        self.caller.db.intake_step = 3

        self.caller.msg(
            f'The clerk dips a quill and writes "|w{display_name}|n" into the '
            "legal ledger with deliberate strokes. A faint amber seal pulses "
            "once across the ink.\n\n"
            f'|yClerk:|n "Name filed and sealed. |w{display_name}|n. '
            "Do not attempt to change it. Move along — Identity Gallery is "
            "to the |wsouth|n.\""
        )

        exit_obj = self.caller.search("south", candidates=self.caller.location.exits, quiet=True)
        if exit_obj:
            self.caller.move_to(exit_obj[0].destination, quiet=True)
            self.caller.execute_cmd("look")


# ---------------------------------------------------------------------------
# Step 3 — Choose Race (Identity Gallery)
# ---------------------------------------------------------------------------

class CmdChooseRace(Command):
    """
    Select your lineage in the Identity Gallery.

    Usage:
      choose <lineage>
      lineages          (to see all options)

    Only works in the Identity Gallery.
    """

    key = "choose"
    aliases = ["select", "lineages", "races"]
    help_category = "OASMC Intake"

    def func(self):
        loc_step = self.caller.location.db.intake_step if self.caller.location else None

        # Show race list if in Identity Gallery without an arg, or if 'lineages'/'races' used
        if loc_step == 3 and (not self.args.strip() or self.cmdstring in ("lineages", "races")):
            self.caller.msg(_race_list())
            return

        # Show class list if in Aptitude Annex
        if loc_step == 4 and (not self.args.strip() or self.cmdstring in ("lineages", "races")):
            self.caller.msg(_class_list())
            return

        if loc_step not in (3, 4):
            self.caller.msg("There is nothing to choose here.")
            return

        choice = self.args.strip().lower()

        # --- Race selection (step 3) ---
        if loc_step == 3:
            if choice not in RACES:
                self.caller.msg(
                    f"|rUnknown lineage: '{choice}'|n\n" + _race_list()
                )
                return

            race_data = RACES[choice]
            self.caller.db.race = choice
            self.caller.db.intake_step = 4

            self.caller.msg(
                f"You rest your hand on the plaque beneath the "
                f"|y{race_data['display']}|n banner. It pulses once — warm, "
                f"steady — and the etch glows amber for a moment before fading.\n\n"
                f"|xA quiet voice from somewhere:|n \"{race_data['desc']}\"\n\n"
                "Your lineage has been noted. Proceed to the "
                "|wAptitude Annex|n to the |wsouth|n."
            )

            exit_obj = self.caller.search("south", candidates=self.caller.location.exits, quiet=True)
            if exit_obj:
                self.caller.move_to(exit_obj[0].destination, quiet=True)
                self.caller.execute_cmd("look")

        # --- Class selection (step 4) ---
        elif loc_step == 4:
            if choice not in CLASSES:
                self.caller.msg(
                    f"|rUnknown discipline: '{choice}'|n\n" + _class_list()
                )
                return

            class_data = CLASSES[choice]
            self.caller.db.char_class = choice
            self.caller.db.intake_step = 5

            self.caller.msg(
                f"You press your palm against the |y{class_data['display']}|n tablet. "
                "The seal ignites amber, reading you in a way that is difficult "
                "to describe — like something already knew.\n\n"
                f"|x{class_data['desc']}|n\n\n"
                "Your discipline has been recorded. Proceed to the "
                "|wOath & Stamp Station|n to the |wsouth|n to finalize your intake."
            )

            exit_obj = self.caller.search("south", candidates=self.caller.location.exits, quiet=True)
            if exit_obj:
                self.caller.move_to(exit_obj[0].destination, quiet=True)
                self.caller.execute_cmd("look")


# ---------------------------------------------------------------------------
# Step 5 — Confirm / Reconsider (Oath & Stamp Station)
# ---------------------------------------------------------------------------

class CmdConfirmIntake(Command):
    """
    Finalize your intake and receive your Academy Intake Token.

    Usage:
      confirm

    Type `reconsider` if you want to go back and change your choices.
    Only works in the Oath & Stamp Station.
    """

    key = "confirm"
    aliases = ["finalize", "stamp"]
    help_category = "OASMC Intake"

    def func(self):
        if not _in_intake_step(self.caller, 5):
            self.caller.msg("There is nothing to confirm here.")
            return

        race = self.caller.db.race
        char_class = self.caller.db.char_class

        if not race or not char_class:
            self.caller.msg(
                "Your intake record is incomplete. Return to the Name Registry "
                "and complete all steps before confirming."
            )
            return

        race_display = RACES[race]["display"]
        class_display = CLASSES[char_class]["display"]
        instructor = CLASSES[char_class]["instructor"]

        # Issue token
        tokens = spawn("ACADEMY_INTAKE_TOKEN")
        if tokens:
            token = tokens[0]
            token.location = self.caller
            # Personalize the token desc
            token.db.desc = (
                f"A small warded disc of pale grey stone. The surface is etched "
                f"with |w{self.caller.key}|n in silver script, alongside "
                f"|y{race_display}|n and |y{class_display}|n, sealed beneath "
                f"a faint amber glow. A Compliance stamp on the reverse reads: "
                f"|yANUVARA OASMC – INTAKE CERTIFIED|n. "
                "It hums faintly near the Neutral Corridor checkpoint."
            )

        self.caller.db.intake_complete = True

        self.caller.msg(
            "The Registrar — a compact woman with ink-stained fingers and the "
            "expression of someone who has stamped more lives than she can count "
            "— lifts a warded die-press and brings it down on a grey disc.\n\n"
            "The impact rings like a small bell.\n\n"
            f"|yRegistrar:|n \"Sealed. |w{self.caller.key}|n. "
            f"|y{race_display}|n. |y{class_display}|n. Intake date recorded.\"\n\n"
            "She slides the disc across the counter. It glows once — amber — "
            "then settles into something permanent.\n\n"
            f"|yRegistrar:|n \"Congratulations. You are now officially a person.\"\n\n"
            "She turns back to her ledger without further ceremony.\n\n"
            "|w[You receive an Academy Intake Token.]|n\n\n"
            "Proceed north to the |wNeutral Corridor Checkpoint|n. "
            "Present your token to the guard. Once through, find the "
            f"|w{instructor}|n instructor in the Academy wing and deliver your token "
            "to begin your training."
        )


class CmdReconsider(Command):
    """
    Go back and reconsider your intake choices before they are finalized.

    Usage:
      reconsider

    Only works in the Oath & Stamp Station, before you confirm.
    """

    key = "reconsider"
    aliases = ["go back", "back"]
    help_category = "OASMC Intake"

    def func(self):
        if not _in_intake_step(self.caller, 5):
            self.caller.msg(
                "There is nothing to reconsider here. "
                "You are only allowed to second-guess yourself at the Oath & Stamp Station."
            )
            return

        if self.caller.db.intake_complete:
            self.caller.msg(
                "|yRegistrar:|n \"The token has been stamped. "
                "It is done. There is no 'reconsider' after the stamp.\""
            )
            return

        # Ask what they want to reconsider
        self.caller.msg(
            "|yRegistrar:|n \"Hmm.\" She sets down the press and regards you "
            "with the patience of someone billing by the hour.\n\n"
            "\"What, specifically, do you wish to reconsider?\"\n\n"
            "  |wreconsider race|n    — Return to the Identity Gallery\n"
            "  |wreconsider class|n   — Return to the Aptitude Annex\n"
            "  |wreconsider name|n    — Return to the Name Registry (rare, but possible)"
        )

    def parse(self):
        self.target = self.args.strip().lower()

    def func(self):
        if not _in_intake_step(self.caller, 5):
            self.caller.msg("There is nothing to reconsider here.")
            return

        if self.caller.db.intake_complete:
            self.caller.msg(
                '|yRegistrar:|n "The stamp is applied. You are a person. '
                "Live with it.\""
            )
            return

        target = self.args.strip().lower()

        destinations = {
            "race": ("Identity Gallery", 3),
            "lineage": ("Identity Gallery", 3),
            "class": ("Aptitude Annex", 4),
            "discipline": ("Aptitude Annex", 4),
            "name": ("Name Registry", 2),
        }

        if target not in destinations:
            self.caller.msg(
                "Reconsider |wrace|n, |wclass|n, or |wname|n?"
            )
            return

        room_name, step = destinations[target]
        room = self.caller.search(room_name, global_search=True, quiet=True)
        if room:
            self.caller.db.intake_step = step
            self.caller.move_to(room[0], quiet=True)
            self.caller.execute_cmd("look")
        else:
            self.caller.msg(
                f"(Could not locate {room_name} — ask a Warden for directions.)"
            )


# ---------------------------------------------------------------------------
# CmdSet — bundled so default_cmdsets can import in one line
# ---------------------------------------------------------------------------

class OASMCIntakeCmdSet(CmdSet):
    """All commands needed for the OASMC diegetic character creation flow."""

    key = "OASMCIntakeCmdSet"

    def at_cmdset_creation(self):
        self.add(CmdBeginIntake())
        self.add(CmdSetName())
        self.add(CmdChooseRace())
        self.add(CmdConfirmIntake())
        self.add(CmdReconsider())
