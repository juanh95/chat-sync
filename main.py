from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import users, chat, access
from config import database

database.connect_db_with_mongoengine()

origins = ["http://localhost:5173"] 
# Create an instance of a FastAPI app 
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (adjust as needed)
    allow_headers=["*"],  # Allow all headers (adjust as needed)
)

# Attach the user routes 
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(access.router)