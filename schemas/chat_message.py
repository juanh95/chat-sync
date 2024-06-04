from pydantic import BaseModel, Field
from datetime import datetime

class ChatMessage(BaseModel):
    recipient: str = Field(..., description="Username of the message recipient")
    sender: str = Field(..., description="Username of the message sender")
    message: str = Field(..., description="The content of the message")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="UTC timestamp of message creation (ISO 8601 format)")