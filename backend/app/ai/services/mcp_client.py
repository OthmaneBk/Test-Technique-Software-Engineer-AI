import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "model"))
from groqLLM import GroqLLM
from Prompt import prompt
MCP_SERVER_PATH = Path(__file__).resolve().parent / "mcp_server.py"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prompts"))
from system_prompt import SYSTEM_PROMPT

MAX_ITERATION_DEFAULT = 5


def build_message(role: str, content: str) -> dict:
    return {"role": role, "content": prompt(content).message}


class MCP_CLIENT:

    def __init__(self, MAX_ITERATION=MAX_ITERATION_DEFAULT):
        self.MAX_ITERATION = MAX_ITERATION

    async def ask(self, question: str, history: list[dict] | None = None) -> str:
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(MCP_SERVER_PATH)],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                mcp_tools = await session.list_tools()
                formatted_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    }
                    for tool in mcp_tools.tools
                ]

                llm = GroqLLM()
                messages = [build_message("system", SYSTEM_PROMPT) ]
                
                for turn in (history or []):
                    messages.append(build_message(turn["role"], turn["content"]))

                messages.append(build_message("user", question),)
                
                response_tool = llm.chat(messages=messages, tools=formatted_tools)
                count = 0
                result = response_tool["content"]   
                while response_tool["tool_calls"] and count < self.MAX_ITERATION:
                    count += 1
                    messages.append(response_tool["message"])

                    for tool_call in response_tool["tool_calls"]:
                        tool_call_id = tool_call["id"]
                        func_name = tool_call["function"]["name"]
                        func_args = tool_call["function"]["arguments"]
                        result_mcp = await session.call_tool(func_name, json.loads(func_args))
                        result_text = "\n".join(part.text for part in result_mcp.content if hasattr(part, "text"))

                        messages.append({
                            "tool_call_id": tool_call_id,
                            "role": "tool",
                            "name": func_name,
                            "content": prompt(result_text).message,
                        })

                    response_tool = llm.chat(messages=messages, tools=formatted_tools)
                    result = response_tool["content"]

        return result