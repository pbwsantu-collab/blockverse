# BLOCKVERSE

Original 3D voxel sandbox survival game in Python (Ursina Engine).

**Not a Minecraft clone** — original design, names, systems, and art direction.

## Features

- Procedural chunk-streamed world (16×128×16 chunks)
- Multi-octave terrain (continents, hills, beaches, oceans, deserts, forests, mountains, tundra)
- Sparse trees + basic caves + coal/iron ores
- Face-culled chunk meshing (no per-voxel entities)
- Visible water surfaces
- First-person controller (walk, sprint, jump, fly)
- Mining & building
- Inventory + hotbar with stacking
- Hand crafting (wood → planks, torch, tools)
- Survival stats with **visual bars** (health, hunger, stamina, XP)
- Day/night cycle + seasons foundation
- Weather state (clear / cloudy / rain / snow)
- Torch placement with glow markers
- Wandering creatures + melee combat
- Creative / Survival modes
- F3 debug overlay
- F5/F9 quicksave/load
- Data-driven blocks, items, recipes, biomes
- Event bus + modular OOP architecture

## Run

```bash
git clone https://github.com/pbwsantu-collab/blockverse.git
cd blockverse
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Requires a desktop display (OpenGL).

## Controls

| Key | Action |
|-----|--------|
| WASD | Move |
| Space | Jump / fly up |
| Left Shift | Sprint |
| Mouse | Look |
| LMB | Break block / Attack creature |
| RMB | Place block |
| 1–9 | Select hotbar |
| C | Craft (planks → torch → tools) |
| G | Toggle Creative / Survival |
| F3 | Debug overlay |
| Ctrl+F | Toggle fly |
| F5 / F9 | Quicksave / Quickload |
| Esc | Unlock mouse |
| Q | Quit |

## Project layout

```
blockverse/
  main.py
  config/          # blocks, items, recipes, biomes, game settings
  engine/          # event bus, time/seasons
  world/           # chunks, terrain, meshing, noise
  blocks/          # block registry
  player/          # inventory, stats
  crafting/        # recipe system
  survival/        # health, hunger helpers
  graphics/        # lighting helpers
  ui/              # HUD helpers
  save/            # save manager
  ...
```

## Roadmap (modular – add without rewriting core)

- Full voxel light propagation
- Flowing water simulation
- Villages + NPC schedules
- Quests, skills, trading
- SQLite world persistence
- Mod API + multiplayer-ready interfaces

## License

Original project. Do not use Minecraft assets or proprietary designs.
