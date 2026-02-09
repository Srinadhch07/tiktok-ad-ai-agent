from fastapi import APIRouter, HTTPException, Request, Depends
from app.auth.user_auth_dependency import get_current_user
from app.schemas.ad_schema import AdPayload

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/music/validate/{music_id}")
def validate_music(music_id: str,request: Request):
    payload = request.state.payload
    if "music.read" not in payload["scope"]:
        raise HTTPException(status_code=403, detail="Missing music permission")

    if not music_id.startswith("valid"):
        raise HTTPException(status_code=400, detail="Invalid music ID")
    return {"valid": True}


@router.post('/ad/create')
async def create_ad(payload: AdPayload, request: Request):
    try:
        user_details = request.state.payload
        ad_details = payload
        if user_details["region"] == "IN":
            raise HTTPException(403, "Geo-restriction")
        if ad_details.objective.lower() == "conversions" and not ad_details.music_id:
            raise HTTPException(400, "Music is required for conversions")
        return {"data": {"status": "Success", "ad_id": "ad_1821"}}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Internal server error at create_ad(): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
