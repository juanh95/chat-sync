from pymongo import MongoClient
from mongoengine import connect, StringField, IntField, Document
import json

def test_connection_pymongo(connection_string):
  """Tests connection to MongoDB Atlas using pymongo."""
  try:
    client = MongoClient(connection_string)
    print("Connection successful using pymongo!")
    client.close()
  except Exception as e:
    print("Connection failed using pymongo:", e)

def test_connection_mongoengine(connection_string):
   """Tests connection to MongoDB Atlas using MongoEngine."""
   try:
      client = MongoClient(connection_string)
      db = client.get_database("ChatSync")
      connect(db=db.name, host=connection_string)

      class User(Document):
         name = StringField(required=True)
         age = IntField()

      # Create sample data
      data1 = User(name="John Doe", age=30)
      data2 = User(name="Jane Smith", age=25)

      # Save the data to the collection

      data1.save()
      data2.save()
      print("Data saved successfully!")
      print("Connection successful using MongoEngine!")
   except Exception as e:  # Catch other potential errors
      print("An error occurred:", e)
   finally:
      if client:
         client.close()

if __name__ == "__main__":
  # Load MongoDB credentials from the JSON file 
   with open("db_creds.json", "r") as rf: 
      db_creds = json.load(rf)

   username = db_creds['username']
   password = db_creds['password']

   # Replace with your actual connection string from MongoDB Atlas
   connection_string = f'mongodb+srv://{username}:{password}@test-cluster-1.r089son.mongodb.net/?retryWrites=true&w=majority'

   # Test connection using pymongo
   test_connection_pymongo(connection_string)

   # Test connection using MongoEngine
   test_connection_mongoengine(connection_string)

