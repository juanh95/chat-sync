from pydantic import BaseModel, Field
from fastapi import WebSocket

class UserWebSocket(BaseModel):
    websocket: WebSocket
    username: str

    model_config = {
            "arbitrary_types_allowed": True
        } 