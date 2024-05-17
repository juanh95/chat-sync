from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path, Query, HTTPException, WebSocketException, status
import json
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_CODE = os.environ.get("ACCESS_CODE")

router = APIRouter()

class ConnectionManager: 
   def __init__(self):
      self.active_connections: list[WebSocket] = []

   async def connect(self, websocket: WebSocket):
      await websocket.accept() 
      self.active_connections.append(websocket)

   def disconnect(self, websocket: WebSocket):
      self.active_connections.remove(websocket)
   
   async def send_personal_message(self, message: str, websocket:WebSocket):
      await websocket.send_text(message)

   async def broadcast(self, message: str):
      for connection in self.active_connections:
         await connection.send_text(message)

manager = ConnectionManager()

async def check_access_code(access_code: str = Query(None)):
    """
    Checks if the provided access code is valid.
    """
    if access_code != ACCESS_CODE:
      raise WebSocketException(code=4001, reason="Invalid access code")

@router.websocket("/chat/{username}")
async def web_socket_endpoint(websocket: WebSocket, username: str, access_code: str = Query(None, description="The access code of the week")):
   await check_access_code(access_code)
   try:
      await manager.connect(websocket)
      while True:
         data = await websocket.receive_text()
         # await manager.send_personal_message(f"You wrote {data}", websocket)
         await manager.broadcast(f'{username} said: {data}')
   except WebSocketDisconnect: 
      manager.disconnect(websocket)
      await manager.broadcast(f"{username} left the chat")
   