"""Face-culled mesh builder for a chunk (Ursina Mesh)."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .chunk import Chunk
    from blocks.block_registry import BlockRegistry

FACES = [
    ((0, 1, 0), [(0,1,0),(1,1,0),(1,1,1),(0,1,1)]),
    ((0,-1, 0), [(0,0,0),(0,0,1),(1,0,1),(1,0,0)]),
    ((1, 0, 0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
    ((-1,0, 0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
    ((0, 0, 1), [(0,0,1),(0,1,1),(1,1,1),(1,0,1)]),
    ((0, 0,-1), [(0,0,0),(1,0,0),(1,1,0),(0,1,0)]),
]

def build_mesh_data(chunk: "Chunk", registry: "BlockRegistry"):
    verts, tris, cols = [], [], []
    size, height = chunk.size, chunk.height
    blocks = chunk.blocks

    def solid(x, y, z) -> bool:
        if x < 0 or y < 0 or z < 0 or x >= size or y >= height or z >= size:
            return False
        bid = int(blocks[x, y, z])
        if bid == 0:
            return False
        b = registry.get(bid)
        if b and b.transparent:
            return False
        return True

    for x in range(size):
        for y in range(height):
            for z in range(size):
                bid = int(blocks[x, y, z])
                if bid == 0:
                    continue
                bdef = registry.get(bid)
                if bdef and bdef.transparent and not bdef.solid:
                    continue
                color = registry.color(bid)
                for (dx, dy, dz), corners in FACES:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if solid(nx, ny, nz):
                        continue
                    base = len(verts)
                    for cx, cy, cz in corners:
                        verts.append((x + cx + chunk.cx * size, y + cy, z + cz + chunk.cz * size))
                        cols.append(color)
                    tris.extend([base, base+1, base+2, base, base+2, base+3])
    return verts, tris, cols
