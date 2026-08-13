from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infra.database import get_db

from app.schemas.login import LoginRequest, TokenResponse
from app.services.user_service import UserService
from app.core.security import encode

router = APIRouter(
    prefix="/auths",
    tags=["Auths"],
)


@router.post(
    "/",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = UserService.authenticate(
        db,
        data.email,
        data.password,
    )

    token = encode(
        str(user.id),
    )

    return {
        "access_token": token,
        "token": "bearer",
    }
