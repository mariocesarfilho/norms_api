from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_model import User

class UserRepository:
    @staticmethod
    def create(db: Session, user: User) -> User:
        try:
            db.add(user)
            db.commit()
            db.refresh(user)

            return user
        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        user = db.execute(
            select(User).where(
                User.email == email
            )
        )

        return user.scalar_one_or_none()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)