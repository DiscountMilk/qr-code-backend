from fastapi import APIRouter
from .project_endpoint import router as projects_router
from .scan_endpoint import router as scan_router
from .qr_code_endpoint import router as qr_code_router

router = APIRouter(prefix="/v1")
router.include_router(projects_router)
router.include_router(scan_router)
router.include_router(qr_code_router)
