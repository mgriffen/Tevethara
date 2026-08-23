# -*- coding: utf-8 -*-
"""
Connection screen

This is the text to show the user when they first connect to the game (before
they log in).

To change the login screen in this module, do one of the following:

- Define a function `connection_screen()`, taking no arguments. This will be
  called first and must return the full string to act as the connection screen.
  This can be used to produce more dynamic screens.
- Alternatively, define a string variable in the outermost scope of this module
  with the connection string that should be displayed. If more than one such
  variable is given, Evennia will pick one of them at random.

The commands available to the user when the connection screen is shown
are defined in evennia.default_cmds.UnloggedinCmdSet. The parsing and display
of the screen is done by the unlogged-in "look" command.

⚠️ Horizontal rules only — no ║ sides. In the web client every output line is
its own div at line-height 1.6, so a vertical box edge draws as a stack of
disconnected dashes with gaps between the rows. Horizontal rules are unaffected
by line-height and hold up in every font that carries the U+2500 block.
"""

_WIDTH = 70
_INDENT = ""


def _rule(char, color="|x"):
    return "{}{}{}|n".format(_INDENT, color, char * _WIDTH)


def _centered(text, visible_width):
    return _INDENT + " " * ((_WIDTH - visible_width) // 2) + text


def connection_screen():
    """Return the pre-login notice shown to every connecting session."""
    return "\n".join(
        [
            "",
            _rule("═"),
            "",
            _centered("|wT E V E T H A R A|n", 17),
            "",
            _INDENT + "|cAnuvara Bay|n |x— Passenger Terminal, Berth Nine|n",
            _rule("─", "|x"),
            "",
            _INDENT + "The ferry to the |cOASMC|n island departs on the tide.",
            _INDENT + "Passengers are asked to present themselves at the desk",
            _INDENT + "before boarding.",
            "",
            _INDENT + "    Returning passenger     |wconnect|n |x<name> <password>|n",
            _INDENT + "    First crossing          |wcreate|n |x<name> <password>|n",
            "",
            _INDENT + "|xNames containing spaces must be enclosed in quotation marks.|n",
            _INDENT + "|xType|n |whelp|n |xfor assistance, or|n |wlook|n |xto read this again.|n",
            "",
            _rule("═"),
            "",
        ]
    )
