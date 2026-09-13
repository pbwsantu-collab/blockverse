"""Data-driven block registry."""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

@dataclass
class BlockDef:
    id: int
    name: str
    solid: bool = True
    transparent: bool = False
    hardness: float = 1.0
    color: list[float] = field(default_factory=lambda: [0.5, 0.5, 0.5])
    drops: str | None = None
    tool: str | None = None
    light: int = 0

class BlockRegistry:
    def __init__(self) -> None:
        self._by_id: dict[int, BlockDef] = {}
        self._by_name: dict[str, BlockDef] = {}

    def load(self, path: str | Path) -> None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for key, props in data.items():
            b = BlockDef(
                id=int(props["id"]),
                name=props.get("name", key),
                solid=props.get("solid", True),
                transparent=props.get("transparent", False),
                hardness=float(props.get("hardness", 1.0)),
                color=list(props.get("color", [0.5, 0.5, 0.5])),
                drops=props.get("drops"),
                tool=props.get("tool"),
                light=int(props.get("light", 0)),
            )
            self._by_id[b.id] = b
            self._by_name[key] = b
            self._by_name[b.name.lower()] = b

    def get(self, id_or_name: int | str) -> BlockDef | None:
        if isinstance(id_or_name, int):
            return self._by_id.get(id_or_name)
        return self._by_name.get(str(id_or_name).lower())

    def color(self, block_id: int) -> tuple[float, float, float]:
        b = self._by_id.get(block_id)
        if not b:
            return (0.5, 0.5, 0.5)
        c = b.color
        return (float(c[0]), float(c[1]), float(c[2]))

registry = BlockRegistry()
