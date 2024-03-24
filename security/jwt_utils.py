from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.users import User
from datetime import timedelta, datetime

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # Define token URL

def verify_password(plain_password: str, hashed_password: str) -> bool:
   return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
   to_encode = data.copy()
   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire.timestamp()})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(
      status_code=401,
      detail="Invalid authentication credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )

   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("username")
      if username is None:
         raise credentials_exception
      return User.objects.get(username=username)
   except JWTError:
      raise credentials_exception
