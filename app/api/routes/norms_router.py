from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.norm import NormCreate, NormResponse
from app.services.norm_service import NormService

router = APIRouter(
    prefix="/norms",
    tags=["Norms"]
)

@router.post("/", response_model=NormResponse, status_code=status.HTTP_201_CREATED)
def create_norm(data: NormCreate, db: Session = Depends(get_db)):

    norm = NormService.create(db, data)
    return {
        "success": True,
        "message": "Criado Norma com sucesso!",
        "data": norm
    }
