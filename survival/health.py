"""Health subsystem."""
from __future__ import annotations

class HealthSystem:
    def __init__(self, max_hp: float = 20.0) -> None:
        self.max_hp = max_hp
        self.hp = max_hp

    def damage(self, amount: float) -> float:
        self.hp = max(0.0, self.hp - amount)
        return self.hp

    def heal(self, amount: float) -> float:
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp

    @property
    def alive(self) -> bool:
        return self.hp > 0
