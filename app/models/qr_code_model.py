from pydantic import BaseModel, Field

class QRCodeCreate(BaseModel):
    pass

class QRCodeResponse(BaseModel):
    id: int
    project_id: int
    latitude: float
    longitude: float
    scan_count: int = Field(0, description="Total number of scans")

