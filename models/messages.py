from mongoengine import StringField, DateTimeField, ObjectIdField
from models.base_model import MongoBaseModel

class Message(MongoBaseModel):
   message_text = StringField(required=True)
   from_user_id = ObjectIdField(required=True)
   to_user_id = ObjectIdField(required=True)
   date_time = DateTimeField(required=True)

   meta = {
      'collection' : 'messages'
   }

   def create(self):
      return self.save()

