from datetime import datetime
from app.models.models import UserCreate, UserResponse, UserUpdate

class UserService:
    """
    User service handling business logic for user operations.
    In a real application, this would interact with a database.
    """
    
    def __init__(self):
        # Simulated in-memory database
        self.users_db: list[UserResponse] = []
        self.next_id = 1
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if username already exists
        if any(u.username == user.username for u in self.users_db):
            raise ValueError(f"Username '{user.username}' already exists")
        
        # Create new user
        new_user = UserResponse(
            id=self.next_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=datetime.now()
        )
        
        self.users_db.append(new_user)
        self.next_id += 1
        return new_user
    
    async def get_user(self, user_id: int) -> UserResponse | None:
        """Get a user by ID"""
        return next((u for u in self.users_db if u.id == user_id), None)
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Get all users with pagination"""
        return self.users_db[skip : skip + limit]
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse | None:
        """Update a user's information"""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        # Update only provided fields
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.full_name is not None:
            user.full_name = user_update.full_name
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        user = await self.get_user(user_id)
        if not user:
            return False
        
        self.users_db.remove(user)
        return True

# Singleton instance
user_service = UserService()
