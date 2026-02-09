from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

async def create_access_token(client_id: str, region: str = "US"):
    if not client_id.startswith("valid_client"):
        raise HTTPException(401,"Invalid client Id")
    payload = {
        "scope": ["ads.create", "music.read"],
        "region": region,
        "exp": datetime.utcnow() + timedelta(minutes=10)  
    }
    token = jwt.encode(payload,SECRET, algorithm=ALGORITHM)
    return token

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(401, "Invalid or expired token")




