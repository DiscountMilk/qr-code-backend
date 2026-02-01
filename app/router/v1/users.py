from fastapi import APIRouter, HTTPException, Query
from app.models.models import UserCreate, UserResponse, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    - **username**: Unique username (3-50 characters)
    - **email**: User email address
    - **full_name**: Optional full name
    """
    try:
        return await user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return")
):
    """
    Get all users with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    return await user_service.get_all_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Get a specific user by ID.
    """
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Update a user's information.
    Only provided fields will be updated.
    """
    user = await user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """
    Delete a user.
    """
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return None
