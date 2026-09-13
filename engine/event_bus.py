"""Simple pub/sub event bus."""
from __future__ import annotations
from collections import defaultdict
from typing import Any, Callable

class EventBus:
    def __init__(self) -> None:
        self._subs: dict[str, list[Callable[..., None]]] = defaultdict(list)

    def on(self, event: str, handler: Callable[..., None]) -> None:
        self._subs[event].append(handler)

    def off(self, event: str, handler: Callable[..., None]) -> None:
        if handler in self._subs[event]:
            self._subs[event].remove(handler)

    def emit(self, event: str, **kwargs: Any) -> None:
        for h in list(self._subs.get(event, [])):
            try:
                h(**kwargs)
            except Exception as e:
                print(f"[EventBus] handler error on {event}: {e}")

bus = EventBus()
