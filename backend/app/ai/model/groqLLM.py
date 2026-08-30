import os
import sys

from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "interface"))
from LLM import LLM

load_dotenv()
GROQ_MODEL = os.getenv("GROQ_MODEL", "")


class GroqLLM(LLM):

    def __init__(self):
        self.model_name = GROQ_MODEL
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def chat(self, messages: list[dict], tools: list[dict] = None, temperature: float = 0, max_tokens:int = 1000) -> dict:
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens":max_tokens
        }
        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        message_dict = message.model_dump()
        clean_message = {
            "role": message_dict["role"],
            "content": message_dict["content"],
        }
        if message_dict.get("tool_calls"):
            clean_message["tool_calls"] = message_dict["tool_calls"]
        return {
            "content": message.content,
            "tool_calls": message_dict["tool_calls"],
            "message": clean_message,
        }
