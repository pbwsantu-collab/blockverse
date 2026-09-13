"""World clock: day/night and seasons."""
from __future__ import annotations

class TimeManager:
    def __init__(self, day_length: float = 1440.0) -> None:
        self.day_length = day_length
        self.time = 0.25 * day_length
        self.paused = False

    def update(self, dt: float) -> None:
        if not self.paused:
            self.time = (self.time + dt) % self.day_length

    @property
    def day_fraction(self) -> float:
        return self.time / self.day_length

    @property
    def is_day(self) -> bool:
        f = self.day_fraction
        return 0.25 <= f < 0.75

    @property
    def sun_intensity(self) -> float:
        f = self.day_fraction
        if 0.25 <= f < 0.75:
            return max(0.0, 1.0 - abs(f - 0.5) * 4)
        return 0.05

    @property
    def season_index(self) -> int:
        return int((self.time / self.day_length) * 4) % 4

    @property
    def season_name(self) -> str:
        return ("Spring", "Summer", "Autumn", "Winter")[self.season_index]
