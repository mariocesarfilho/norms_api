from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService.create(db, data)