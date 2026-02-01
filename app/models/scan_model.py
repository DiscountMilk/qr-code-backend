from datetime import datetime
from pydantic import BaseModel, Field

class ScanResponse(BaseModel):
    id: int
    qr_code_id: int
    scanned_at: datetime
    ip_address: str
    user_agent: str
    device_type: str
    browser: str
    os: str

class ScanCreate(BaseModel):
    qr_code_id: int
    ip_address: str
    user_agent: str
    device_type: str
    browser: str
    os: str

