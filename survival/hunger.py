"""Hunger / food subsystem."""
from __future__ import annotations

class HungerSystem:
    def __init__(self, max_hunger: float = 20.0) -> None:
        self.max_hunger = max_hunger
        self.hunger = max_hunger

    def drain(self, amount: float) -> None:
        self.hunger = max(0.0, self.hunger - amount)

    def feed(self, amount: float) -> None:
        self.hunger = min(self.max_hunger, self.hunger + amount)

    @property
    def starving(self) -> bool:
        return self.hunger <= 0
