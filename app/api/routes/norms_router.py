from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.norm import NormCreate, NormResponse, NormListResponse, NormUpdate, NormDeleteResponse
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

@router.get("/{norm_id}", response_model=NormResponse)
def get_norm(norm_id: int, db: Session = Depends(get_db)):
    norm = NormService.get_by_id(db, norm_id)

    return {
        "success": True,
        "message": "Norma encontrada com sucesso!",
        "data": norm,
    }

@router.get("/", response_model=NormListResponse)
def get_all_norms(db: Session = Depends(get_db)):
    norms = NormService.get_all(db)

    return {
        "success": True,
        "message": "Normas encontradas com sucesso!",
        "data": norms,
    }

@router.patch ("/{norm_id}", response_model=NormUpdate)
def update_norm(norm_id: int, data: NormUpdate, db: Session = Depends(get_db)):
    norm = NormService.update(db, norm_id, data)

    return {
        "success": True,
        "message": "Norma atualizada com sucesso!",
        "data": norm,
    }

@router.delete("/{norm_id}", response_model=NormDeleteResponse)
def delete_norm(norm_id: int, db: Session = Depends(get_db)):
    NormService.delete(db, norm_id)

    return{
        "success": True,
        "message": "Norma deletada com sucesso!",
    }