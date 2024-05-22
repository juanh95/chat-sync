from mongoengine import *
from models.base_model import MongoBaseModel

class User(MongoBaseModel):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)

    meta = {
        'collection': 'users'  # Specify the collection name (optional)
    }

    def create(self): 
        return self.save() 
   
    @classmethod
    def find(cls, field: str, value: str):  # Type hints for clarity
        """Finds a User object by the specified field and value."""
        try:
            if field == "username":
                return cls.objects.filter(username=value).first()
            elif field == "id":
                return cls.objects.get(id=value)  # Use get() for ID lookup
            else:
                raise ValueError(f"Invalid field for search: '{field}'")  # More informative message
        except (ValueError, User.DoesNotExist):  # Catch both ValueError and DoesNotExist
            return None



    @classmethod
    def find_by_username(cls, target_username):
        return cls.objects.filter(username=target_username).first()

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"