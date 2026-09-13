# BLOCKVERSE

Original 3D voxel sandbox survival game in Python (Ursina Engine).

**Not a Minecraft clone** — original design, names, systems, and art direction.

## Features (current prototype)

- Procedural chunk-streamed world (16×128×16 chunks)
- Multi-octave terrain (continents, hills, beaches, oceans)
- Sparse trees + basic caves
- Face-culled chunk meshing (no per-voxel entities)
- First-person controller (walk, sprint, jump, fly)
- Mining & building
- Inventory + hotbar with stacking
- Hand crafting (wood → planks)
- Survival stats (health, hunger, stamina, XP)
- Day/night cycle + seasons foundation
- Weather state (clear / cloudy / rain / snow)
- Wandering creatures + melee combat
- Creative / Survival modes
- F3 debug overlay
- F5/F9 quicksave/load
- Data-driven blocks & items
- Event bus + modular OOP architecture

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| WASD | Move |
| Space | Jump |
| Left Shift | Sprint |
| Mouse | Look |
| LMB | Break block / Attack |
| RMB | Place block |
| 1–9 | Select hotbar |
| F3 | Debug overlay |
| Ctrl+F | Toggle fly |
| F5 / F9 | Quicksave / Quickload |
| C | Craft (planks/torch/tools) |
| G | Toggle creative/survival |
| Esc | Unlock mouse |
| Q | Quit |

## Architecture

Modular packages: `engine/`, `world/`, `blocks/`, `items/`, `player/`, `crafting/`, `entities/`, `ui/`, `save/`, …

Designed for expansion: lighting, water, biomes, villages, NPCs, quests, mods, multiplayer-ready interfaces.

## License

Original project. Do not use Minecraft assets or proprietary designs.
