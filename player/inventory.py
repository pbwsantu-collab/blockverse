"""Hotbar + inventory with stacking."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ItemStack:
    item_id: str
    count: int = 1
    durability: int | None = None

    def copy(self) -> "ItemStack":
        return ItemStack(self.item_id, self.count, self.durability)

class Inventory:
    def __init__(self, slots: int = 36, hotbar_size: int = 9) -> None:
        self.slots: list[ItemStack | None] = [None] * slots
        self.hotbar_size = hotbar_size
        self.selected = 0

    def hotbar(self) -> list[ItemStack | None]:
        return self.slots[: self.hotbar_size]

    def selected_stack(self) -> ItemStack | None:
        return self.slots[self.selected]

    def add(self, item_id: str, count: int = 1, max_stack: int = 64) -> int:
        for i, s in enumerate(self.slots):
            if s and s.item_id == item_id and s.count < max_stack:
                space = max_stack - s.count
                take = min(space, count)
                s.count += take
                count -= take
                if count <= 0:
                    return 0
        for i, s in enumerate(self.slots):
            if s is None:
                take = min(max_stack, count)
                self.slots[i] = ItemStack(item_id, take)
                count -= take
                if count <= 0:
                    return 0
        return count

    def consume_selected(self, amount: int = 1) -> bool:
        s = self.selected_stack()
        if not s or s.count < amount:
            return False
        s.count -= amount
        if s.count <= 0:
            self.slots[self.selected] = None
        return True
