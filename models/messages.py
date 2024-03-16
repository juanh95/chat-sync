from mongoengine import * 

class Message(Document):
   message_text = StringField(required=True)
   from_user_id = ObjectIdField(required=True)
   to_user_id = ObjectIdField(required=True)
   date_time = DateTimeField(required=True)

   meta = {
      'collection' : 'messages'
   }

