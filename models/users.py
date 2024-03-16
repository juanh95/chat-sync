from mongoengine import *

class User(Document):
   username = StringField(required=True, unique=True)
   password = StringField(required=True)
   email = StringField(required=True, unique=True)

   meta = {
      'collection': 'users'  # Specify the collection name (optional)
   }
