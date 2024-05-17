import os

ACCESS_CODE_FROM_OS = os.environ.get("ACCESS_CODE")

def verify_access_code(access_code:str) -> bool:
   if access_code == os.environ.get("ACCESS_CODE"): return True
   else: return False