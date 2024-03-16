from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

# Load MongoDB credentials from the JSON file 
with open("backup_creds.json", "r") as rf: 
    db_creds = json.load(rf)

username = db_creds['username']
password = db_creds['password']

uri = f'mongodb+srv://{username}:{password}@chatsync-cluster.0bqxu4h.mongodb.net/?retryWrites=true&w=majority&appName=ChatSync-Cluster'

# Connection Feedback Message 
print("Connecting to MongoDB instance...")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)