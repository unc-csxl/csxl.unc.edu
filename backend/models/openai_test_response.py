from pydantic import BaseModel


class OpenAITestResponse(BaseModel):
    """Response model for OpenAI test endpoint."""

    last_name: str
    jersey_number: int
