from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

class UserService:
    @staticmethod
    def create(db: Session, data: UserCreate) -> User:
        user = User(
            email=data.email,
            password_hash=data.password_hash
        )

        return UserRepository.create(db, user)


    