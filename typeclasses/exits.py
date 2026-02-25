"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set pointing to the room it leads to, but it may also have other properties
like `aliases` for multi-directional traversal.

Custom exit typeclasses can be set per-exit in the batch script or via
the `@typeclass` command.

"""

from evennia.objects.objects import DefaultExit

from .objects import ObjectParent


class Exit(ObjectParent, DefaultExit):
    """
    Exits are connectors between Rooms. An exit always has a destination
    property set pointing to the room it leads to. Exits are traversed
    with the `go` command or by typing the exit's name / alias directly.
    """

    pass


class TokenGatedExit(ObjectParent, DefaultExit):
    """
    A special exit that requires the player to carry an Academy Intake Token
    (tagged 'intake_token' in category 'oasmc') before they can pass.

    Used for the Neutral Corridor checkpoint between the Compliance side
    and the Academy side of the OASMC complex.
    """

    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        Check for a valid intake token before allowing traversal.
        Superusers (admins) bypass the check automatically.
        """
        if traversing_object.is_superuser:
            return super().at_traverse(traversing_object, target_location, **kwargs)

        has_token = traversing_object.search(
            "Academy Intake Token",
            candidates=traversing_object.contents,
            quiet=True,
        )
        if not has_token:
            traversing_object.msg(
                "A Compliance Guard steps into your path, one hand raised.\n"
                '|yGuard:|n "Token. No token, no entry. Return to the Registry '
                "and complete your intake before you're allowed through.\"\n"
                "The gate remains firmly closed."
            )
            return False

        return super().at_traverse(traversing_object, target_location, **kwargs)
