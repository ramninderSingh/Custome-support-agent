import json
from pathlib import Path
from typing import Any

class JSONStore:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read(self)-> list[dict[str, Any]]:
        with open(self.file_path, "r" , encoding = "utf-8") as f:
            return json.load(f)

    def write(self, data: list[dict[str, Any]]) -> None:
        with open(self.file_path, "w", encoding = "utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
