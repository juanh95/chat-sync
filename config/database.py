import json 
import os
from mongoengine import connect, Document, StringField
from pymongo import MongoClient

def connect_db_with_mongoengine():
   # Use string interpolation to compose connection string
   connection_string = f'mongodb+srv://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@chatsync-cluster.0bqxu4h.mongodb.net/?retryWrites=true&w=majority'

   try:
      # Feedback Message
      print("Connecting to MongoDB through MongoEngine...")

      # Client Connection
      client = MongoClient(connection_string)

      # Selecting the database we're going to use
      db = client.get_database(os.environ.get("DATABASE_NAME"))

      # Connecting to it via MongoEngine
      connect(db=db.name, host=connection_string)

      # Positive feedback message
      print("Connection successful")
   except Exception as e:
      print("An error occurred:", e)

