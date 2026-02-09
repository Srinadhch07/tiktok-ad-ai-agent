from pydantic import BaseModel
from typing import Optional

class AdPayload(BaseModel):
    campaign_name: str
    objective: str
    ad_text: str
    cta: str
    music_id: Optional[str] = None