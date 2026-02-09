from fastapi import Request, HTTPException
from .oauth import verify_token

async def get_current_user(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing")
        token = auth_header.split(" ")[1]
        token = token.strip().replace('"', '')
        payload = await verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Payload not found")
        # adding payload to state
        request.state.payload = payload
        return payload
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")