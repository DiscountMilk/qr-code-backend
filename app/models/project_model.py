from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    target_url: HttpUrl = Field(..., description="URL where QR codes redirect to")

class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    target_url: HttpUrl | None = None
    is_active: bool | None = None

class ProjectResponse(BaseModel):
    id: int
    user_id: str
    name: str
    target_url: str
    is_active: bool
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime