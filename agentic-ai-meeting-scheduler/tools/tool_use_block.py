## inspired from anthropic cook book - https://github.com/pixegami/claude-booking-bot/blob/main/tools/tools.py

from pydantic import BaseModel
from typing_extensions import Literal

class ToolUseBlock(BaseModel):
    id: str

    input: object ## this is dict containing all the input and values

    name: str

    type: Literal["tool_use"]