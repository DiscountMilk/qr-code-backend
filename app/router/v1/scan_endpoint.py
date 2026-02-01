from fastapi import APIRouter
from app.models.scan_model import *

router = APIRouter(prefix="/projects/{project_id}/{qrcode}", tags=["Scans"])

@router.post("/", response_model=ScanResponse ,status_code=201)
async def create_scan(scan: ScanCreate) -> ScanResponse:
    pass

@router.get("/", response_model=ScanResponse, status_code=200)
async def get_scans() -> list[ScanResponse]:
    pass

@router.get("/{scan_id}", response_model=ScanResponse ,status_code=200)
async def get_scan(scan_id: int) -> ScanResponse:
    pass





