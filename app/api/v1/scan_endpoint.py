from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user_id
from app.models.scan_model import *

router = APIRouter(prefix="/qrcodes", tags=["Scans"])

@router.post("/{qrcode_id}/scans", response_model=ScanResponse, status_code=201)
async def create_scan(qrcode_id: int, scan: ScanCreate, user_id: str = Depends(get_current_user_id)) -> ScanResponse:
    pass

@router.get("/{qrcode_id}/scans", response_model=list[ScanResponse], status_code=200)
async def get_scans(qrcode_id: int, user_id: str = Depends(get_current_user_id)) -> list[ScanResponse]:
    pass

@router.get("/{qrcode_id}/scans/{scan_id}", response_model=ScanResponse, status_code=200)
async def get_scan(qrcode_id: int, scan_id: int, user_id: str = Depends(get_current_user_id)) -> ScanResponse:
    pass

# Get all scans for a project
@router.get("/projects/{project_id}/scans", response_model=list[ScanResponse], status_code=200)
async def get_project_scans(project_id: int, user_id: str = Depends(get_current_user_id)) -> list[ScanResponse]:
    """Get all scans for all QR codes in a project (for analytics)"""
    pass