from pydantic import BaseModel
from typing import Optional, List

class AccessTokenPayload(BaseModel):
    client_id: str
    region : Optional[str] = "US"
