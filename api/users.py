from fastapi import APIRouter, Depends, HTTPException

from models.users import User
from utils import password_utils
from security.jwt_utils import verify_password, create_access_token

router = APIRouter()

@router.post("/user/signup")
async def signup(user_data: dict):
   # Check if the username already exists 
   existing_user = User.objects.filter(username=user_data["username"]).first() 
   if existing_user:
      raise HTTPException(status_code=400, detail="Username already exists")

   # Hash the password and re-assign the value to the user data object that came in 
   hashed_password = password_utils.hash_password(user_data["password"])
   user_data["password"] = hashed_password

   try: 
      user = User(**user_data).create()

      # Create a dictionary containing the desired fields
      response_data = {"message": "User created successfully", "data": {}}
      response_data["data"]["username"] = user.username
      response_data["data"]["email"] = user.email
      
      return response_data
   except Exception as e: 
      print(f"Error creating user: {e}")
      raise HTTPException(status_code=500, detail="Internal server error")
   
@router.post("/user/login")
async def login(login_data: dict): 
   username = login_data.get("username")
   password = login_data.get("password")

   if not username or not password: 
      raise HTTPException(status_code=400, detail="Username or password is missing")
   
   user = User.objects.filter(username=username).first()
   if not user:
      raise HTTPException(status_code=400, detail="Invalid username or password")
   
   if not verify_password(password, user.password):
      raise HTTPException(status_code=400, detail="Invalid username or password")
   
   access_token = create_access_token({"username": user.username})
   return {"access_token": access_token, "token_type": "bearer"}




   

   