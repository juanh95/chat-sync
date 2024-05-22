from mongoengine import StringField
from models.base_model import MongoBaseModel

"""
User Model

Represents a user in the MongoDB database.

Fields:
    username (str): The user's unique username.
    password (str): The user's hashed password.
    email (str): The user's email address (must be unique).

Methods:
    find(field: str, value: str) -> User or None:
        Finds a user by a specified field (either "username" or "id") and value.
        Returns the User object if found, or None if not found.

    create() -> User:
        Saves the user to the database and returns the saved User object.

    __str__() -> str:
        Returns a string representation of the user in the format 
        "User(username='<username>', email='<email>')".

Attributes:
    meta (dict): Metadata for the MongoEngine model.
        - collection (str): The name of the MongoDB collection to use for this model.

Inheritance:
    MongoBaseModel: A custom base model for MongoEngine documents with additional functionality 
                   (e.g., conversion to/from Pydantic models).
"""
class User(MongoBaseModel):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)

    meta = {
        'collection': 'users'  # Specify the collection name (optional)
    }
    
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
    
    def create(self): 
        return self.save() 

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"