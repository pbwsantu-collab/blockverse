"""Save/load facade (quicksave uses JSON; SQLite planned)."""
from pathlib import Path
import json

class SaveManager:
    def __init__(self, folder: str | Path = "saves"):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def write_json(self, name: str, data: dict) -> None:
        path = self.folder / f"{name}.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(path)

    def read_json(self, name: str) -> dict | None:
        path = self.folder / f"{name}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
