from fastapi import APIRouter, Depends, HTTPException, Response
from app.auth import get_current_user_id
from app.services.qr_code_service import QRCodeService
from app.models.qr_code_model import *

router = APIRouter(prefix="/projects/{project_id}/qrcodes", tags=["QR Codes"])
qr_code_service = QRCodeService()

@router.post("/", response_model=QRCodeResponse, status_code=201)
async def create_qr_code(
    project_id: int, qr_code: QRCodeCreate, user_id: str = Depends(get_current_user_id)
) -> QRCodeResponse:
    """Generate a new QR code for the project"""
    if qr_code.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project id mismatch")
    return await qr_code_service.create_qr_code(project_id, user_id)

@router.get("/", response_model=list[QRCodeResponse], status_code=200)
async def get_qr_codes(
    project_id: int,
    include_deleted: bool = False,
    user_id: str = Depends(get_current_user_id),
) -> list[QRCodeResponse]:
    """Get all QR codes for a project. Set include_deleted=True for analytics."""
    return await qr_code_service.get_qr_codes(project_id, user_id, include_deleted)

@router.get("/{qrcode_id}", response_model=QRCodeResponse, status_code=200)
async def get_qr_code(
    project_id: int, qrcode_id: int, user_id: str = Depends(get_current_user_id)
) -> QRCodeResponse:
    qr_code = await qr_code_service.get_qr_code(project_id, qrcode_id, user_id)
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qr_code

@router.patch("/{qrcode_id}", response_model=QRCodeResponse, status_code=200)
async def update_qr_code(
    project_id: int,
    qrcode_id: int,
    qr_code: QRCodeUpdate,
    user_id: str = Depends(get_current_user_id),
) -> QRCodeResponse:
    updated = await qr_code_service.update_qr_code(project_id, qrcode_id, qr_code, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="QR code not found")
    return updated

@router.delete("/{qrcode_id}", status_code=204)
async def delete_qr_code(
    project_id: int, qrcode_id: int, user_id: str = Depends(get_current_user_id)
):
    """Soft delete: Sets deleted_at and is_active=False. Scan data is preserved."""
    deleted = await qr_code_service.delete_qr_code(project_id, qrcode_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="QR code not found")
    return Response(status_code=204)
