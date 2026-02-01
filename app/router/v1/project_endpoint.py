from fastapi import APIRouter
from app.models.project_model import *


router = APIRouter(prefix="/projects", tags=["QR Codes"])

@router.post("/", response_model=ProjectResponse ,status_code=201)
async def create_project(project: ProjectCreate) -> ProjectResponse:
    pass

@router.get("/", response_model=ProjectResponse, status_code=200)
async def get_projects() -> list[ProjectResponse]:
    pass

@router.get("/{project_id}", response_model=ProjectResponse ,status_code=200)
async def get_project(project_id: int) -> ProjectResponse:
    pass

@router.delete("/{project_id}", status_code=200)
async def delete_project(project_id: int) -> ProjectResponse:
    pass



