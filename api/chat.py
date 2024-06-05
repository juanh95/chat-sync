from fastapi import Depends, APIRouter, WebSocket, WebSocketDisconnect, Path, Query, HTTPException, WebSocketException, status
import json
from dotenv import load_dotenv
import os
from schemas.chat_message import ChatMessage
from typing import Dict, List
from utils.utils import get_current_user_from_jwt
from jose import JWTError

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
      if websocket in self.active_connections:
         return self.active_connections.pop(websocket)
      else:
         print("Websocket not found in active connections")
         return None
         
   async def send_room_message(self, chat_message_data: ChatMessage):
      for connection in self.active_connections.keys():
         await connection.send_json(chat_message_data.model_dump())
         
   async def broadcast(self, message: str):
      for connection in self.active_connections.keys():
         await connection.send_json({'message': message, 'broadcast': True})

manager = ConnectionManager()

@router.websocket("/chat/{username}")
async def web_socket_endpoint(websocket: WebSocket, username: str):
   try:
      await websocket.accept()
      print("Accepted the connection")

      authenticated = False
      
      print("Waiting to receive initial JSON")
      data = await websocket.receive_json()

      token = data.get("token")

      if not token: 
         raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token") 

      print("Token was present")
      
      try: 
         print("About to verify JWT")
         sender_username = await get_current_user_from_jwt(token)
         print(f"Done verifying JWT, the sender_username is {sender_username}")

         if sender_username != username:
            print("----- Got into the if evaluation")
            websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Credentials")
         
         authenticated = True

         print("Token was validated")

      except JWTError or WebSocketDisconnect:
         websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid Authentication")
      
      if authenticated: 
         while True:
            print("Regular chat in progress")
            data = await websocket.receive_json()
            chat_message_data = ChatMessage(**data)
            
            await manager.send_room_message(chat_message_data)
      else: 
         await websocket.send_json({"message": "Authentication failed"})
         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
   
   except WebSocketDisconnect: 
      
      disconnected_username = manager.disconnect(websocket)

      if disconnected_username != None:
         await manager.broadcast(f"{disconnected_username} left the chat")
   