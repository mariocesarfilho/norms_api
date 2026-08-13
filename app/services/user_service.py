from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


class UserService:

    @staticmethod
    def create(
        db: Session,
        data: UserCreate
    ) -> User:
        user_existing = UserRepository.get_by_email(
            db, data.email
        )

        if user_existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este usuário já existe"
            )

        hashed_password = hash_password(
            data.password
        )

        user = User(
            email=data.email,
            password_hash=hashed_password
        )

        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str
    ) -> User:
        user = UserRepository.get_by_email(
            db, email
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais Inválidas"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais Inválidas"
            )

        return user
