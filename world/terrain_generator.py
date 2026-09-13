"""Procedural terrain + trees + simple caves + ores."""
from __future__ import annotations
import numpy as np
from .noise_util import fbm, value_noise_2d
from .chunk import Chunk

AIR, GRASS, DIRT, STONE, SAND, WATER = 0, 1, 2, 3, 4, 5
WOOD, LEAVES, PLANKS, COBBLE, COAL_ORE, IRON_ORE = 6, 7, 8, 9, 10, 11
SEA_LEVEL = 62

def height_at(wx: float, wz: float, seed: int) -> int:
    cont = fbm(wx * 0.003, wz * 0.003, seed, octaves=5)
    hills = fbm(wx * 0.02, wz * 0.02, seed + 7, octaves=3)
    detail = fbm(wx * 0.08, wz * 0.08, seed + 13, octaves=2)
    h = 48 + cont * 40 + hills * 18 + detail * 4
    return int(np.clip(h, 8, 120))

def biome_at(wx: float, wz: float, seed: int) -> str:
    temp = fbm(wx * 0.004, wz * 0.004, seed + 99)
    hum = fbm(wx * 0.004, wz * 0.004, seed + 199)
    h = height_at(wx, wz, seed)
    if h < SEA_LEVEL - 2:
        return "ocean"
    if h > 90:
        return "mountains"
    if temp > 0.7 and hum < 0.35:
        return "desert"
    if temp < 0.3:
        return "tundra"
    if hum > 0.6:
        return "forest"
    return "plains"

def generate_chunk(chunk: Chunk, seed: int) -> None:
    size, height = chunk.size, chunk.height
    base_x, base_z = chunk.cx * size, chunk.cz * size
    for lx in range(size):
        for lz in range(size):
            wx, wz = base_x + lx, base_z + lz
            h = height_at(wx, wz, seed)
            bio = biome_at(wx, wz, seed)
            surface = SAND if bio == "desert" else (STONE if bio == "mountains" else GRASS)
            fill = SAND if bio == "desert" else DIRT
            for y in range(height):
                if y > h:
                    chunk.blocks[lx, y, lz] = WATER if y <= SEA_LEVEL else AIR
                elif y == h:
                    chunk.blocks[lx, y, lz] = surface if h >= SEA_LEVEL - 1 else SAND
                elif y > h - 4:
                    chunk.blocks[lx, y, lz] = fill
                else:
                    chunk.blocks[lx, y, lz] = STONE
                    n = value_noise_2d(wx * 0.15, y * 0.15 + wz * 0.01, seed + 50)
                    if y < 40 and n > 0.82:
                        chunk.blocks[lx, y, lz] = COAL_ORE
                    if y < 28 and n > 0.90:
                        chunk.blocks[lx, y, lz] = IRON_ORE
            for y in range(5, min(h - 2, 50)):
                cave = fbm(wx * 0.05, y * 0.08 + wz * 0.05, seed + 77, octaves=3)
                if cave > 0.72:
                    chunk.blocks[lx, y, lz] = AIR
            if h >= SEA_LEVEL and bio in ("plains", "forest", "tundra"):
                tree_chance = 0.08 if bio == "forest" else 0.02
                if value_noise_2d(wx * 0.5, wz * 0.5, seed + 33) > (1.0 - tree_chance):
                    if chunk.get(lx, h, lz) in (GRASS, DIRT):
                        trunk_h = 4 + int(value_noise_2d(wx, wz, seed + 44) * 3)
                        for ty in range(1, trunk_h + 1):
                            if h + ty < height:
                                chunk.set(lx, h + ty, lz, WOOD)
                        top = h + trunk_h
                        for dx in range(-2, 3):
                            for dz in range(-2, 3):
                                for dy in range(-1, 3):
                                    if abs(dx) + abs(dz) + abs(dy) > 4:
                                        continue
                                    nx, ny, nz = lx + dx, top + dy, lz + dz
                                    if 0 <= nx < size and 0 <= ny < height and 0 <= nz < size:
                                        if chunk.get(nx, ny, nz) == AIR:
                                            chunk.set(nx, ny, nz, LEAVES)
    chunk.dirty = True
