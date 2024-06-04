from fastapi import Depends, APIRouter, WebSocket, WebSocketDisconnect, Path, Query, HTTPException, WebSocketException, status
import json
from dotenv import load_dotenv
import os
from schemas.chat_message import ChatMessage
from typing import Dict, List

load_dotenv()

router = APIRouter()

CONNECTIONS = {}

class ConnectionManager: 
   def __init__(self):
      self.active_connections: Dict[WebSocket, str] = CONNECTIONS

   async def connect(self, websocket: WebSocket, username: str):
      await websocket.accept() 
      self.active_connections[websocket] = username

   def disconnect(self, websocket: WebSocket):
      return self.active_connections.pop(websocket)

   async def send_room_message(self, chat_message_data: ChatMessage):
      for connection in self.active_connections.keys():
         await connection.send_json(chat_message_data.model_dump())
         
   async def broadcast(self, message: str):
      for connection in self.active_connections.keys():
         await connection.send_json({'message': message, 'broadcast': True})

manager = ConnectionManager()

@router.websocket("/chat/{username}")
async def web_socket_endpoint(websocket: WebSocket, username: str):
   
   # token = websocket.headers.get("Authorization")
   
   # if not token or not token.startswith("Bearer"):
   #    raise WebSocketException(code=4001, reason="Invalid Token")
   
   # token = token[7:] # strip off the "Bearer" prefix

   # username = await get_current_user_from_jwt(token)

   # if not username:
   #    raise WebSocketException(code=4001, reason="Invalid Authentication Credentials")
   
   try:
      await manager.connect(websocket, username)
      
      while True:
         # TODO: Handle when data isn't received this way
         data = await websocket.receive_json()
         chat_message_data = ChatMessage(**data)
         
         await manager.send_room_message(chat_message_data)
   
   except WebSocketDisconnect: 
      
      disconnected_username = manager.disconnect(websocket)

      await manager.broadcast(f"{disconnected_username} left the chat")
   