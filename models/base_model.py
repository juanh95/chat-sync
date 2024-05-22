from mongoengine import Document
from pydantic import BaseModel

"""
MongoBaseModel

A base class for MongoEngine documents enabling integration with Pydantic models.

Class Methods:

- `from_pydantic`: Creates a MongoEngine document from a Pydantic model.
- `to_pydantic`: Converts a MongoEngine document to a Pydantic model.

This facilitates data validation using Pydantic and persistence using MongoEngine.
"""

class MongoBaseModel(Document):
    meta = {'abstract': True}  # This makes it a base model, not a collection

    @classmethod
    def from_pydantic(cls, pydantic_model: BaseModel):
        """Creates a MongoEngine document from a Pydantic model."""
        return cls(**pydantic_model.model_dump())
    
    def to_pydantic(self) -> BaseModel:
        """Converts the MongoEngine document to a Pydantic model."""
        return self.__class__.model_validate(self.to_mongo().to_dict())
