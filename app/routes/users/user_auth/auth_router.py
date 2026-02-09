from fastapi import APIRouter, HTTPException, Request, Depends
from app.auth.oauth import create_access_token
from dotenv import load_dotenv
from app.schemas.access_token_schema import AccessTokenPayload
import os

load_dotenv()

router = APIRouter()

@router.post('/oauth/token')
async def get_token(payload: AccessTokenPayload, request: Request):
    try:
        token = await create_access_token(payload.client_id , payload.region)
        return {"data": { "access_token" : token }}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Internal server error at get_token(): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
