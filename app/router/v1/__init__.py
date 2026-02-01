from fastapi import APIRouter
from .users import router as users_router
from .products import router as products_router

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(products_router)
