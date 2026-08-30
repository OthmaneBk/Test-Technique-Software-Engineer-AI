from abc import ABC, abstractmethod

class LLM(ABC):

    @abstractmethod
    def chat(self, messages: list[dict], tools: list[dict] = None, temperature: float = 0) -> dict:
        pass
