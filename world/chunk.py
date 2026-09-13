"""Chunk storage: dense 3D array of block IDs."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field

@dataclass
class Chunk:
    cx: int
    cz: int
    size: int = 16
    height: int = 128
    blocks: np.ndarray = field(default=None)
    dirty: bool = True
    mesh_entity: object | None = None

    def __post_init__(self) -> None:
        if self.blocks is None:
            self.blocks = np.zeros((self.size, self.height, self.size), dtype=np.uint8)

    def get(self, x: int, y: int, z: int) -> int:
        if 0 <= x < self.size and 0 <= y < self.height and 0 <= z < self.size:
            return int(self.blocks[x, y, z])
        return 0

    def set(self, x: int, y: int, z: int, block_id: int) -> None:
        if 0 <= x < self.size and 0 <= y < self.height and 0 <= z < self.size:
            self.blocks[x, y, z] = block_id
            self.dirty = True

    def key(self) -> tuple[int, int]:
        return (self.cx, self.cz)
