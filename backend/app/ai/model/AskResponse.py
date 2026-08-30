from pydantic import BaseModel

class AskResponse(BaseModel):
    answer: str | None = None
    action: str | None = None