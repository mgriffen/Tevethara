"""
Tevethara prototype package.

Each submodule registered in settings.PROTOTYPE_MODULES contributes its
module-level dicts to the global prototype registry. Module-defined
prototypes are read-only at runtime — that's the canon-content guarantee.
"""
