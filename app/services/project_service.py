from app.database import supabase
from app.models.project_model import ProjectCreate, ProjectUpdate, ProjectResponse
from fastapi import HTTPException

class ProjectService:
    """
    Project service handling business logic for project operations.
    Interacts with Supabase as the database.
    """

    async def create_project(self, project: ProjectCreate, user_id: str) -> ProjectResponse:
        """Create a new project"""
        data = project.model_dump()
        data["user_id"] = user_id
        response = supabase.table("projects").insert(data).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return ProjectResponse(**response.data[0])

    async def get_project(self, project_id: int, user_id: str) -> ProjectResponse | None:
        """Get a project by ID"""
        response = supabase.table("projects").select("*").eq("id", project_id).eq("user_id", user_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        if not response.data:
            return None
        return ProjectResponse(**response.data[0])

    async def get_all_projects(self, user_id: str) -> list[ProjectResponse]:
        """Get all projects"""
        response = supabase.table("projects").select("*").eq("user_id", user_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return [ProjectResponse(**item) for item in response.data]

    async def update_project(self, project_id: int, project_update: ProjectUpdate, user_id: str) -> ProjectResponse | None:
        """Update a project's information"""
        data = {k: v for k, v in project_update.model_dump().items() if v is not None}
        response = supabase.table("projects").update(data).eq("id", project_id).eq("user_id", user_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        if not response.data:
            return None
        return ProjectResponse(**response.data[0])

    async def delete_project(self, project_id: int, user_id: str) -> bool:
        """Delete a project"""
        response = supabase.table("projects").delete().eq("id", project_id).eq("user_id", user_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return bool(response.data)