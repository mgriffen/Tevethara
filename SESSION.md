# Session Handoff — 2026-03-04

## Where We Left Off

### What's Working
- ASCII box-draw room header renders on `look` (box-draw chars, yellow name, cyan exits)
- Text prompt (`<HP:100/100 ST:100/100 MP:50/50>`) sends after every command and on login
- Right sidebar layout: main pane (2/3) + right panel (1/3) with `[ Map ]` and `[ World ]` boxes
- HUD chrome (header bar + status bar) collapsed by default, `[HUD]` button top-right toggles it
- `@mapset` builder command works (`@mapset <area> <x> <y>`, `@mapset/show`, `@mapset/clear`)
- Map render system (`world/map_render.py`) complete — coordinate-based, viewport 21×13 chars
- OOB pipeline works: server → `tev_map` OOB → JS `oob` event handler → `updateMap()`

### What Still Needs Doing Before Map Works End-to-End

**CRITICAL — run this in-game first thing:**
```
@batchcommands world.map_setup
```
The coordinate batch was re-fixed (changed `caller` → `self` in all @py lines).
You should see "Tagged: Arrival Pier", "Tagged: Pierside Queue", etc.
After that, moving rooms should populate the map panel.

### Open Map Issues to Revisit
- `_get_area_rooms()` in `world/map_render.py` uses `search_object("*", typeclass=...)` —
  if this doesn't return all rooms reliably, swap to Django ORM:
  ```python
  from evennia.objects.models import ObjectDB
  rooms = ObjectDB.objects.filter(db_typeclass_path="typeclasses.rooms.Room")
  ```
- Map shows `[ No map data ]` until coordinates are tagged (above batch fixes this)
- `[ World ]` panel is wired up (JS `appendWorldEvent()`) but nothing sends to it yet

## Key Files Changed This Session

| File | Change |
|------|--------|
| `typeclasses/rooms.py` | `return_appearance()` with box-draw ASCII header |
| `typeclasses/characters.py` | `get_prompt()`, `update_prompt()`, `send_map()`, `at_after_move()` |
| `commands/command.py` | `at_post_cmd()` sends prompt after every command |
| `commands/map_commands.py` | NEW — `@mapset` builder command |
| `commands/default_cmdsets.py` | Registered `CmdMapSet` |
| `world/map_render.py` | NEW — coordinate-based ASCII map renderer |
| `world/map_setup.ev` | NEW — batch to tag all existing rooms with coordinates |
| `world/apply_map_coords.py` | NEW — Python script alternative to batch |
| `web/templates/webclient/webclient.html` | Right sidebar added, HUD toggle button |
| `web/static/webclient/css/custom.css` | Full layout restructure, pane borders, sidebar styles |
| `web/static/webclient/js/tevethara_ui.js` | OOB handler, HUD toggle, map/world update methods |

## Next Session Candidates
1. Verify map renders after running `@batchcommands world.map_setup`
2. If `_get_area_rooms` still returns empty, swap to Django ORM query (see above)
3. Wire `[ World ]` panel to actual server events (moon phases, server announcements)
4. Moon system implementation (`world/moons.py`, `MoonClock` script, `commands/moon.py`)
5. Phase 1 ranged combat (`shoot`, two-stage aim)
