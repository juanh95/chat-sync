import os
from jose import jwt, JWTError
from typing import Optional

ACCESS_CODE_FROM_OS = os.environ.get("ACCESS_CODE")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

def verify_access_code(access_code:str) -> bool:
   if access_code == os.environ.get("ACCESS_CODE"): return True
   else: return False

async def get_current_user_from_jwt(token: str) -> Optional[str]:
    """Decodes the JWT token and returns the username if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            return None
        return username
    except JWTError:
        return None