from app.database import supabase
from fastapi import HTTPException
from app.models.qr_code_model import QRCodeCreate, QRCodeResponse, QRCodeUpdate
from uuid import uuid4

class QRCodeService:
    async def _project_owned(self, project_id: int, user_id: str) -> bool:
        response = (
            supabase.table("projects")
            .select("id")
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        return bool(response.data)

    async def create_qr_code(self, project_id: int, user_id: str) -> QRCodeResponse:
        if not await self._project_owned(project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")

        data = {
            "project_id": project_id,
            "code": uuid4().hex,
            "is_active": False,
        }
        response = supabase.table("qr_codes").insert(data).execute()
        return QRCodeResponse(**response.data[0])

    async def get_qr_codes(self, project_id: int, user_id: str, include_deleted: bool = False) -> list[QRCodeResponse]:
        if not await self._project_owned(project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")

        query = supabase.table("qr_codes").select("*").eq("project_id", project_id)
        if not include_deleted:
            query = query.eq("deleted_at", None).eq("user_id", user_id)
        response = query.execute()
        return [QRCodeResponse(**item) for item in response.data]

    async def get_qr_code(self, project_id: int, qrcode_id: int, user_id: str) -> QRCodeResponse | None:
        if not await self._project_owned(project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")

        response = (
            supabase.table("qr_codes")
            .select("*")
            .eq("id", qrcode_id)
            .eq("project_id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data:
            return None
        return QRCodeResponse(**response.data[0])

    async def update_qr_code(self, project_id: int, qrcode_id: int, qr_code_update: QRCodeUpdate, user_id: str) -> QRCodeResponse | None:
        if not await self._project_owned(project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")

        data = {k: v for k, v in qr_code_update.dict().items() if v is not None}
        if "project_id" in data and data["project_id"] != project_id:
            if not await self._project_owned(data["project_id"], user_id):
                raise HTTPException(status_code=400, detail="Target project not found")

        response = (
            supabase.table("qr_codes")
            .update(data)
            .eq("id", qrcode_id)
            .eq("project_id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data:
            return None
        return QRCodeResponse(**response.data[0])

    async def delete_qr_code(self, project_id: int, qrcode_id: int, user_id: str) -> bool:
        if not await self._project_owned(project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")

        response = (
            supabase.table("qr_codes")
            .update({"deleted_at": "now()", "is_active": False})
            .eq("id", qrcode_id)
            .eq("project_id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        return bool(response.data)
