"""Simple shapeless crafting from recipes.json."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

class CraftingSystem:
    def __init__(self, recipes_path: str | Path) -> None:
        self.recipes: dict[str, Any] = json.loads(Path(recipes_path).read_text(encoding="utf-8"))

    def try_craft(self, inventory, recipe_key: str) -> bool:
        r = self.recipes.get(recipe_key)
        if not r:
            return False
        inputs = r.get("inputs", {})
        have: dict[str, int] = {}
        for s in inventory.slots:
            if s:
                have[s.item_id] = have.get(s.item_id, 0) + s.count
        for item, need in inputs.items():
            if have.get(item, 0) < need:
                return False
        for item, need in inputs.items():
            left = need
            for i, s in enumerate(inventory.slots):
                if s and s.item_id == item and left > 0:
                    take = min(s.count, left)
                    s.count -= take
                    left -= take
                    if s.count <= 0:
                        inventory.slots[i] = None
        out = r["output"]
        inventory.add(out["item"], out.get("count", 1))
        return True
