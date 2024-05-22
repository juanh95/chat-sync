from pydantic import BaseModel, Field

class BaseUserData(BaseModel):  # Base model with common fields
   username: str = Field(..., description="The user's unique username")
   password: str = Field(..., description="The user's password")

class LoginData(BaseUserData):  # Inherit from BaseUserData
   pass  # No additional fields needed for login

class SignUpData(BaseUserData):  # Inherit from BaseUserData
   email: str = Field(..., description="The user's email address") 
