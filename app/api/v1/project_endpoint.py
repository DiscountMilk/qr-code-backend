from fastapi import APIRouter, Depends, HTTPException, Response
from app.auth import get_current_user_id
from app.models.project_model import *
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

project_service = ProjectService()

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate, user_id: str = Depends(get_current_user_id)) -> ProjectResponse:
    return await project_service.create_project(project, user_id)

@router.get("/", response_model=list[ProjectResponse], status_code=200)
async def get_projects(user_id: str = Depends(get_current_user_id)) -> list[ProjectResponse]:
    return await project_service.get_all_projects(user_id)

@router.get("/{project_id}", response_model=ProjectResponse, status_code=200)
async def get_project(project_id: int, user_id: str = Depends(get_current_user_id)) -> ProjectResponse:
    project = await project_service.get_project(project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=ProjectResponse, status_code=200)
async def update_project(project_id: int, project: ProjectUpdate, user_id: str = Depends(get_current_user_id)) -> ProjectResponse:
    updated = await project_service.update_project(project_id, project, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, user_id: str = Depends(get_current_user_id)):
    """Soft delete: Sets deleted_at and is_active=False"""
    deleted = await project_service.delete_project(project_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return Response(status_code=204)
