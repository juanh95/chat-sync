from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse

from models.users import User
from schemas.auth import LoginData, SignUpData
from utils import password_utils
from security.jwt_utils import verify_password, create_access_token

router = APIRouter()

"""
Creates a new user account.

Args:
    signup_data (SignUpData): A Pydantic model containing the user's signup information:
        * username (str): The desired username (must be unique).
        * password (str): The user's chosen password.
        * email (str): The user's email address (must be unique).

Returns:
    JSONResponse:
        * On Success (201 Created): A JSON response with a success message and the following user data:
            - username (str)
            - email (str)

Raises:
    HTTPException:
        * 400 Bad Request: If the username or email already exists in the database.
        * 500 Internal Server Error: If there's an unexpected error while creating the user 
                                    or saving them to MongoDB.
"""
@router.post("/user/signup")
async def signup(signup_data:SignUpData):
    # Check if the username already exists 
    if User.find(field="username", value=signup_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and re-assign the value to the user data object that came in 
    signup_data.password = password_utils.hash_password(signup_data.password)

    try: 
        created_user = User.from_pydantic(signup_data).create() 
        # Create a dictionary containing the desired fields
        response_data = {"message": "User created successfully", "data": {}}
        response_data["data"]["username"] = created_user.username
        response_data["data"]["email"] = created_user.email
        
        return response_data
    except Exception as e: 
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Unable to save user to MongoDB")

"""
Retrieves information about a user by their ID.

Args:
    user_id (str): The unique identifier of the user to retrieve.

Returns:
    JSONResponse:
        * On Success (200 OK): A JSON response containing the user's ID in the format 
            `{"user_id": "<user_id>"}`.
        * On Failure (404 Not Found): A JSON response indicating that the user with the 
            specified ID was not found.

Raises:
    HTTPException:
        * 404 Not Found: If no user is found with the given `user_id`.
"""
@router.get("/user/{user_id}")
async def get_user(user_id: str):
    existing_user = User.find(field="id", value=user_id)
    if existing_user:
        # Can return more information, TBD
        return (f"user_id: {existing_user.id}")
    else:
        raise HTTPException(status_code=404, detail="User was not found")

"""
Authenticates a user and generates an access token.

Args:
    login_data (LoginData): A Pydantic model containing the user's login credentials:
        - username (str): The user's unique username.
        - password (str): The user's password.

Returns:
    JSONResponse (200 OK): A JSON object containing:
        - access_token (str): A JSON Web Token (JWT) that the client can use 
                              for authenticated requests.
        - token_type (str): Indicates the type of token, which is always "bearer".

Raises:
    HTTPException (400 Bad Request): If the provided credentials are invalid (incorrect username 
                                     or password).
    HTTPException (404 Not Found): If no user is found with the given username.  
"""
@router.post("/user/login")
async def login(login_data:LoginData): 
    user = User.find(field="username",value=login_data.username)

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token({"username": user.username})
    
    response = JSONResponse({"message": "Login successful", "token": access_token})
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Make it HTTP-only for security
        # secure=True  # Send only over HTTPS (in production)
    )

    return response





   

   