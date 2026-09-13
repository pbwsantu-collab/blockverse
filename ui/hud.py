"""HUD helpers – bar drawing as text blocks (Ursina Text)."""
from __future__ import annotations

def bar(current: float, maximum: float, width: int = 10, full: str = "#", empty: str = "-") -> str:
    if maximum <= 0:
        return empty * width
    filled = int(round((current / maximum) * width))
    filled = max(0, min(width, filled))
    return full * filled + empty * (width - filled)

def format_stats(hp: float, max_hp: float, hunger: float, max_hunger: float,
                 stamina: float, max_stamina: float, xp: int, level: int,
                 mode: str, weather: str) -> str:
    return (
        f"HP [{bar(hp, max_hp)}] {hp:.0f}/{max_hp:.0f}\n"
        f"HN [{bar(hunger, max_hunger)}] {hunger:.0f}/{max_hunger:.0f}\n"
        f"ST [{bar(stamina, max_stamina)}] {stamina:.0f}/{max_stamina:.0f}\n"
        f"XP {xp}  Lv{level}  [{mode}]  {weather}"
    )
