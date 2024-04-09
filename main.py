from fastapi import FastAPI

from api import users, chat
from config import database

database.connect_db_with_mongoengine()

# Create an instance of a FastAPI app 
app = FastAPI() 

# Attach the user routes 
app.include_router(users.router)
app.include_router(chat.router)