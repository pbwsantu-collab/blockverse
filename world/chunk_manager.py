"""Load / unload / cache chunks around the player."""
from __future__ import annotations
from typing import Dict, Tuple
from .chunk import Chunk
from .terrain_generator import generate_chunk

class ChunkManager:
    def __init__(self, seed: int = 42, size: int = 16, height: int = 128, render_distance: int = 3) -> None:
        self.seed = seed
        self.size = size
        self.height = height
        self.render_distance = render_distance
        self.chunks: Dict[Tuple[int, int], Chunk] = {}

    def chunk_coords(self, wx: float, wz: float) -> Tuple[int, int]:
        import math
        return (math.floor(wx / self.size), math.floor(wz / self.size))

    def ensure_around(self, wx: float, wz: float) -> list:
        cx, cz = self.chunk_coords(wx, wz)
        needed = set()
        rd = self.render_distance
        for dx in range(-rd, rd + 1):
            for dz in range(-rd, rd + 1):
                needed.add((cx + dx, cz + dz))
        for key in list(self.chunks.keys()):
            if key not in needed:
                ch = self.chunks.pop(key)
                if ch.mesh_entity is not None:
                    try:
                        from ursina import destroy
                        destroy(ch.mesh_entity)
                    except Exception:
                        pass
                    ch.mesh_entity = None
        created = []
        for key in needed:
            if key not in self.chunks:
                ch = Chunk(cx=key[0], cz=key[1], size=self.size, height=self.height)
                generate_chunk(ch, self.seed)
                self.chunks[key] = ch
                created.append(ch)
        return created

    def get_block(self, wx: int, wy: int, wz: int) -> int:
        cx, cz = self.chunk_coords(wx, wz)
        ch = self.chunks.get((cx, cz))
        if not ch:
            return 0
        lx = wx - cx * self.size
        lz = wz - cz * self.size
        return ch.get(lx, wy, lz)

    def set_block(self, wx: int, wy: int, wz: int, block_id: int):
        cx, cz = self.chunk_coords(wx, wz)
        ch = self.chunks.get((cx, cz))
        if not ch:
            return None
        lx = wx - cx * self.size
        lz = wz - cz * self.size
        ch.set(lx, wy, lz, block_id)
        return ch

    def surface_y(self, wx: int, wz: int) -> int:
        for y in range(self.height - 1, -1, -1):
            if self.get_block(wx, y, wz) != 0:
                return y
        return 64
