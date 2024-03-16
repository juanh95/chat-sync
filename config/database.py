import json 
from mongoengine import connect, Document, StringField
from pymongo import MongoClient

def connect_db_with_mongoengine():
   """Connects to the MongoDB instance using credentials from a JSON file.

   Raises:
      FileNotFoundError: If the 'db_creds.json' file is not found.
   """
   try:
      # Load MongoDB credentials from the JSON file
      with open("backup_creds.json", "r") as rf:
         db_creds = json.load(rf)

      # Extract the information into variables
      username = db_creds['username']
      password = db_creds['password']

   except FileNotFoundError as e:
      print(f"Error: Could not find 'db_creds.json' file. Please create it with your MongoDB credentials. {e}")
      return  # Exit the function if credentials file is missing

   # Use string interpolation to compose connection string
   connection_string = f'mongodb+srv://{username}:{password}@chatsync-cluster.0bqxu4h.mongodb.net/?retryWrites=true&w=majority'

   try:
      # Feedback Message
      print("Connecting to MongoDB through MongoEngine...")

      # Client Connection
      client = MongoClient(connection_string)

      # Selecting the database we're going to use
      db = client.get_database("ChatSync")

      # Connecting to it via MongoEngine
      connect(db=db.name, host=connection_string)

      # Positive feedback message
      print("Connection successful")
   except Exception as e:
      print("An error occurred:", e)


# @test-cluster-1.r089son.mongodb.net/
# @chatsync-cluster.0bqxu4h.mongodb.net/
