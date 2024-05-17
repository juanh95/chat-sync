from fastapi import APIRouter, Depends, HTTPException, Response

from utils.utils import verify_access_code

router = APIRouter()

@router.post("/verifyaccesscode")
async def access_code_check(request_data:dict):
   if verify_access_code(request_data.get('access_code')):
      return {'success': True, "access_code": request_data.get('access_code')}
   else: 
      raise HTTPException(status_code=401, detail="Incorrect Access Code")
   