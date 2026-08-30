import json
from pathlib import Path


class HistoryStore:
    DEFAULT_PATH = Path(__file__).resolve().parents[1] / "cache" / "history.json"

    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = path

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        content = self.path.read_text(encoding="utf-8").strip()
        if not content:
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []

    def save(self, history: list[dict]) -> None:
        self.path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

    def append(self, question: str, answer: str) -> None:
        history = self.load()
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        self.save(history)

    def clear(self) -> None:
        self.save([])