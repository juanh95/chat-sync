from mongoengine import *

class User(Document):
   username = StringField(required=True, unique=True)
   password = StringField(required=True)
   email = StringField(required=True, unique=True)

   meta = {
      'collection': 'users'  # Specify the collection name (optional)
   }

   def create(self): 
      self.save() 

   def __str__(self):
      return f"User(username='{self.username}', email='{self.email}')"