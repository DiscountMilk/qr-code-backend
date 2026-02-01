from fastapi import APIRouter
from app.models.qr_code_model import *

router = APIRouter(prefix="/projects/{project_id}/qrcodes", tags=["Projects"])

@router.post("/", response_model=QRCodeResponse, status_code=201)
async def create_qr_code(project_id: int, qr_code: QRCodeCreate) -> QRCodeResponse:
    pass

@router.get("/", response_model=list[QRCodeResponse], status_code=200)
async def get_qr_codes(project_id: int) -> list[QRCodeResponse]:
    pass

@router.get("/{qr_code_id}", response_model=QRCodeResponse, status_code=200)
async def get_qr_code(project_id: int, qr_code_id: int) -> QRCodeResponse:
    pass

@router.delete("/{qr_code_id}", status_code=200)
async def delete_qr_code(project_id: int, qr_code_id: int) -> QRCodeResponse:
    pass

