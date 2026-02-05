from datetime import datetime
from pydantic import BaseModel, Field

class ScanCreate(BaseModel):
    qr_code_id: int
    ip_address: str | None = None
    user_agent: str | None = None
    device_type: str | None = None
    browser: str | None = None
    os: str | None = None
    location: dict | None = Field(None, description="Geographic location data (lat, lon, city, country)")

class ScanResponse(BaseModel):
    id: int
    qr_code_id: int | None
    scanned_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
    device_type: str | None = None
    browser: str | None = None
    os: str | None = None
    location: dict | None = None

