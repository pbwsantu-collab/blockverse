"""Survival stats."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class PlayerStats:
    health: float = 20.0
    max_health: float = 20.0
    hunger: float = 20.0
    max_hunger: float = 20.0
    stamina: float = 20.0
    max_stamina: float = 20.0
    xp: int = 0
    level: int = 1

    def damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def heal(self, amount: float) -> None:
        self.health = min(self.max_health, self.health + amount)

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        while self.xp >= self.level * 20:
            self.xp -= self.level * 20
            self.level += 1
            self.max_health += 2
            self.health = self.max_health
