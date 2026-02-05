from pydantic import BaseModel, Field
from datetime import datetime

class QRCodeCreate(BaseModel):
    project_id: int = Field(..., description="Project ID to associate QR code with")

class QRCodeUpdate(BaseModel):
    project_id: int | None = None
    is_active: bool | None = None
    location: dict | None = Field(None, description="Geographic location data (lat, lon, city, country)")

class QRCodeResponse(BaseModel):
    id: int
    project_id: int | None
    code: str
    is_active: bool
    deleted_at: datetime | None = None
    created_at: datetime
    scan_count: int
    location: dict | None = None