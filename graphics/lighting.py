"""Simple lighting helpers (sun intensity + torch markers)."""
from __future__ import annotations
from typing import Any

class LightingSystem:
    def __init__(self) -> None:
        self.torch_positions: list[tuple[int, int, int]] = []

    def add_torch(self, x: int, y: int, z: int) -> None:
        pos = (x, y, z)
        if pos not in self.torch_positions:
            self.torch_positions.append(pos)

    def remove_torch(self, x: int, y: int, z: int) -> None:
        pos = (x, y, z)
        if pos in self.torch_positions:
            self.torch_positions.remove(pos)

    def sun_color(self, intensity: float) -> tuple[int, int, int, float]:
        return (255, 240, 200, max(0.05, intensity))
