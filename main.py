#!/usr/bin/env python3
"""BLOCKVERSE – Original voxel sandbox survival prototype (Ursina)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from ursina import (
    Ursina, Entity, Text, color, camera, mouse, raycast,
    Vec3, time, application, held_keys, scene, Sky, DirectionalLight,
    AmbientLight, Mesh, destroy, window
)
from ursina.prefabs.first_person_controller import FirstPersonController

from blocks.block_registry import registry
from world.chunk_manager import ChunkManager
from world.chunk_mesher import build_mesh_data
from world.terrain_generator import height_at, biome_at, SEA_LEVEL
from engine.time_manager import TimeManager
from player.inventory import Inventory
from player.stats import PlayerStats
from crafting.crafting_system import CraftingSystem

cfg = json.loads((ROOT / "config" / "game_config.json").read_text(encoding="utf-8"))
registry.load(ROOT / "config" / "blocks.json")
craft = CraftingSystem(ROOT / "config" / "recipes.json")

SEED = int(cfg.get("seed", 42))
CHUNK_SIZE = int(cfg.get("chunk_size", 16))
CHUNK_HEIGHT = int(cfg.get("chunk_height", 128))
RENDER_DIST = int(cfg.get("render_distance", 3))

app = Ursina(
    title=cfg.get("title", "BLOCKVERSE"),
    borderless=False,
    fullscreen=False,
    development_mode=False,
)
window.color = color.rgb(135, 206, 235)
Sky(color=color.rgb(120, 180, 255))

sun = DirectionalLight(shadows=False)
sun.look_at(Vec3(1, -1, 1))
AmbientLight(color=color.rgba(100, 100, 120, 0.4))

chunks = ChunkManager(seed=SEED, size=CHUNK_SIZE, height=CHUNK_HEIGHT, render_distance=RENDER_DIST)
clock = TimeManager(day_length=float(cfg.get("day_length_seconds", 1440)))

spawn_x, spawn_z = 0, 0
chunks.ensure_around(spawn_x, spawn_z)
spawn_y = chunks.surface_y(spawn_x, spawn_z) + 2

player = FirstPersonController(
    position=(spawn_x + 0.5, spawn_y, spawn_z + 0.5),
    speed=cfg.get("player_speed", 6),
    jump_height=cfg.get("jump_force", 8.5) / 10.0,
)
player.gravity = 1
player.cursor.visible = True

inventory = Inventory()
stats = PlayerStats()
inventory.add("wooden_pickaxe", 1)
inventory.add("wooden_sword", 1)
inventory.add("torch", 8)
inventory.add("planks", 16)

gamemode = "survival"
fly_mode = False
debug_on = False
weather = "clear"
weather_timer = 0.0

PLACEABLE = {
    "dirt": 2, "stone": 3, "sand": 4, "wood": 6, "planks": 8,
    "cobble": 9, "torch": 12, "grass": 1,
}

def rebuild_chunk_mesh(ch) -> None:
    if ch.mesh_entity is not None:
        destroy(ch.mesh_entity)
        ch.mesh_entity = None
    verts, tris, cols = build_mesh_data(ch, registry)
    if not verts:
        ch.dirty = False
        return
    mesh = Mesh(vertices=verts, triangles=tris, colors=cols, mode="triangle")
    ent = Entity(model=mesh, collider="mesh")
    ch.mesh_entity = ent
    ch.dirty = False

def refresh_meshes() -> None:
    for ch in chunks.chunks.values():
        if ch.dirty or ch.mesh_entity is None:
            rebuild_chunk_mesh(ch)

refresh_meshes()

class Critter(Entity):
    def __init__(self, position=(0, 70, 0), kind="deer"):
        super().__init__(
            model="cube",
            scale=(0.7, 1.0, 1.2) if kind == "deer" else (0.9, 0.7, 1.0),
            color=color.rgb(160, 120, 60) if kind == "deer" else color.rgb(90, 70, 50),
            position=position,
            collider="box",
        )
        self.kind = kind
        self.hp = 10 if kind == "deer" else 16
        self.speed = 2.5
        self.dir = Vec3(1, 0, 0)
        self.timer = 0.0

    def update(self):
        self.timer -= time.dt
        if self.timer <= 0:
            import random
            ang = random.uniform(0, 6.28)
            self.dir = Vec3(math.cos(ang), 0, math.sin(ang))
            self.timer = random.uniform(1.5, 4.0)
        self.position += self.dir * self.speed * time.dt
        sy = chunks.surface_y(int(self.x), int(self.z)) + 1
        self.y = sy
        if self.hp <= 0:
            destroy(self)

creatures = []

def spawn_creatures_near(px, pz, n=4):
    import random
    for _ in range(n):
        dx = random.randint(-20, 20)
        dz = random.randint(-20, 20)
        sx, sz = int(px) + dx, int(pz) + dz
        sy = chunks.surface_y(sx, sz) + 1
        kind = random.choice(["deer", "boar"])
        creatures.append(Critter(position=(sx + 0.5, sy, sz + 0.5), kind=kind))

spawn_creatures_near(spawn_x, spawn_z)

hotbar_text = Text(text="", position=(-0.85, -0.45), scale=1.0, background=True)
stats_text = Text(text="", position=(-0.85, 0.45), scale=0.9, background=True)
debug_text = Text(text="", position=(-0.85, 0.35), scale=0.75, background=True, enabled=False)
hint = Text(
    text="WASD move | LMB break/attack | RMB place | 1-9 hotbar | F3 debug | F5/F9 save/load | Ctrl+F fly | C craft",
    position=(-0.85, -0.48), scale=0.7, background=True
)

def update_hud():
    hb = []
    for i, s in enumerate(inventory.hotbar()):
        mark = ">" if i == inventory.selected else " "
        if s:
            hb.append(f"{mark}{i+1}:{s.item_id[:6]}x{s.count}")
        else:
            hb.append(f"{mark}{i+1}:--")
    hotbar_text.text = "  ".join(hb)
    mode = "FLY" if fly_mode else gamemode.upper()
    stats_text.text = (
        f"HP {stats.health:.0f}/{stats.max_health:.0f}  "
        f"Hunger {stats.hunger:.0f}  Stam {stats.stamina:.0f}  "
        f"XP {stats.xp} Lv{stats.level}  [{mode}]  {weather}"
    )
    if debug_on:
        px, py, pz = player.x, player.y, player.z
        bio = biome_at(px, pz, SEED)
        debug_text.text = (
            f"FPS {int(1/max(time.dt,1e-4))}  pos {px:.1f},{py:.1f},{pz:.1f}\n"
            f"chunks {len(chunks.chunks)}  biome {bio}  season {clock.season_name}\n"
            f"day {clock.day_fraction:.2f}  seed {SEED}  entities {len(creatures)}"
        )

def input(key):
    global fly_mode, debug_on, gamemode, weather
    if key in "123456789":
        inventory.selected = int(key) - 1
    if key == "f3":
        debug_on = not debug_on
        debug_text.enabled = debug_on
    if key == "f" and held_keys["control"]:
        fly_mode = not fly_mode
        player.gravity = 0 if fly_mode else 1
    if key == "c":
        if craft.try_craft(inventory, "planks_from_wood"):
            stats.add_xp(2)
        elif craft.try_craft(inventory, "torch"):
            stats.add_xp(2)
        elif craft.try_craft(inventory, "wooden_pickaxe"):
            stats.add_xp(5)
        elif craft.try_craft(inventory, "wooden_sword"):
            stats.add_xp(5)
    if key == "g":
        gamemode = "creative" if gamemode == "survival" else "survival"
    if key == "f5":
        quicksave()
    if key == "f9":
        quickload()
    if key == "q":
        application.quit()
    if key == "left mouse down":
        do_break_or_attack()
    if key == "right mouse down":
        do_place()

def do_break_or_attack():
    reach = cfg.get("reach", 5)
    nearest = None
    best = reach
    for c in creatures:
        if not c or not c.enabled:
            continue
        d = (c.position - player.position).length()
        if d < best:
            best = d
            nearest = c
    if nearest and best < 3.5:
        dmg = 4
        sel = inventory.selected_stack()
        if sel and "sword" in sel.item_id:
            dmg = 6
        nearest.hp -= dmg
        stats.add_xp(1)
        if nearest.hp <= 0:
            stats.add_xp(5)
            if nearest in creatures:
                creatures.remove(nearest)
            destroy(nearest)
        return
    hit = raycast(camera.world_position, camera.forward, distance=reach, ignore=(player,))
    if hit.hit:
        n = hit.normal
        bx = int(math.floor(hit.world_point.x - n.x * 0.1))
        by = int(math.floor(hit.world_point.y - n.y * 0.1))
        bz = int(math.floor(hit.world_point.z - n.z * 0.1))
        bid = chunks.get_block(bx, by, bz)
        if bid and bid != 5:
            bdef = registry.get(bid)
            drop = (bdef.drops if bdef and bdef.drops else None)
            name_map = {1: "dirt", 2: "dirt", 3: "cobble", 4: "sand", 6: "wood", 7: None, 8: "planks", 9: "cobble", 10: "coal", 11: "iron_ore"}
            item = drop or name_map.get(bid)
            if item and gamemode == "survival":
                inventory.add(item, 1)
            chunks.set_block(bx, by, bz, 0)
            ch = chunks.chunks.get(chunks.chunk_coords(bx, bz))
            if ch:
                rebuild_chunk_mesh(ch)
            stats.add_xp(1)
            if gamemode == "survival":
                stats.stamina = max(0, stats.stamina - 0.3)

def do_place():
    reach = cfg.get("reach", 5)
    hit = raycast(camera.world_position, camera.forward, distance=reach, ignore=(player,))
    if not hit.hit:
        return
    n = hit.normal
    bx = int(math.floor(hit.world_point.x + n.x * 0.51))
    by = int(math.floor(hit.world_point.y + n.y * 0.51))
    bz = int(math.floor(hit.world_point.z + n.z * 0.51))
    if abs(bx + 0.5 - player.x) < 0.8 and abs(bz + 0.5 - player.z) < 0.8 and abs(by + 0.5 - player.y) < 1.5:
        return
    sel = inventory.selected_stack()
    if not sel:
        return
    block_id = PLACEABLE.get(sel.item_id)
    if not block_id:
        return
    if gamemode == "survival":
        if not inventory.consume_selected(1):
            return
    chunks.set_block(bx, by, bz, block_id)
    ch = chunks.chunks.get(chunks.chunk_coords(bx, bz))
    if ch:
        rebuild_chunk_mesh(ch)

SAVE_PATH = ROOT / "saves" / "quicksave.json"

def quicksave():
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "pos": [player.x, player.y, player.z],
        "stats": stats.__dict__,
        "selected": inventory.selected,
        "hotbar": [({"id": s.item_id, "count": s.count} if s else None) for s in inventory.hotbar()],
        "time": clock.time,
        "weather": weather,
        "gamemode": gamemode,
    }
    SAVE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("[BLOCKVERSE] Quicksave OK")

def quickload():
    global weather, gamemode
    if not SAVE_PATH.exists():
        print("[BLOCKVERSE] No save found")
        return
    data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
    player.position = Vec3(*data["pos"])
    for k, v in data.get("stats", {}).items():
        if hasattr(stats, k):
            setattr(stats, k, v)
    inventory.selected = data.get("selected", 0)
    for i, slot in enumerate(data.get("hotbar", [])):
        if slot:
            from player.inventory import ItemStack
            inventory.slots[i] = ItemStack(slot["id"], slot["count"])
        else:
            inventory.slots[i] = None
    clock.time = data.get("time", clock.time)
    weather = data.get("weather", "clear")
    gamemode = data.get("gamemode", "survival")
    chunks.ensure_around(player.x, player.z)
    refresh_meshes()
    print("[BLOCKVERSE] Quickload OK")

_chunk_refresh = 0.0

def update():
    global _chunk_refresh, weather_timer, weather
    dt = time.dt
    clock.update(dt)
    intensity = clock.sun_intensity
    sun.color = color.rgba(255, 240, 200, intensity)
    if intensity < 0.2:
        window.color = color.rgb(20, 25, 50)
    else:
        window.color = color.rgb(int(100 + 55 * intensity), int(150 + 56 * intensity), int(200 + 35 * intensity))
    weather_timer += dt
    if weather_timer > 120:
        weather_timer = 0
        import random
        weather = random.choice(["clear", "cloudy", "rain", "snow"])
    if gamemode == "survival" and not fly_mode:
        stats.hunger = max(0, stats.hunger - dt * 0.02)
        if stats.hunger <= 0:
            stats.damage(dt * 0.5)
        else:
            stats.stamina = min(stats.max_stamina, stats.stamina + dt * 0.5)
    if held_keys["shift"] and not fly_mode:
        player.speed = cfg.get("player_speed", 6) * cfg.get("sprint_multiplier", 1.6)
        if gamemode == "survival":
            stats.stamina = max(0, stats.stamina - dt * 2)
            if stats.stamina <= 0:
                player.speed = cfg.get("player_speed", 6)
    else:
        player.speed = cfg.get("player_speed", 6) * (2.5 if fly_mode else 1.0)
    if fly_mode and held_keys["space"]:
        player.y += 6 * dt
    _chunk_refresh -= dt
    if _chunk_refresh <= 0:
        _chunk_refresh = 0.4
        created = chunks.ensure_around(player.x, player.z)
        for ch in created:
            rebuild_chunk_mesh(ch)
        for ch in chunks.chunks.values():
            if ch.dirty:
                rebuild_chunk_mesh(ch)
    update_hud()

print("=" * 50)
print("  BLOCKVERSE  –  voxel sandbox prototype")
print("  Seed:", SEED, " |  Mode:", gamemode)
print("=" * 50)
app.run()
