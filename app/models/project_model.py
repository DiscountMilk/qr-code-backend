from pydantic import BaseModel, Field, HttpUrl

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    target_url: HttpUrl = Field(..., description="URL where QR codes redirect to")

class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    target_url: HttpUrl | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    target_url: str
