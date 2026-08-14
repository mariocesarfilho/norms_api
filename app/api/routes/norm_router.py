from fastapi import APIRouter, Depends, HTTPException, status

from app.scrapers.federal_revenue_scraper import (
    FederalRevenueUnavailableError,
    FederalRevenueInvalidResponseError,
)
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.norm import (
    NormCreate,
    NormDeleteResponse,
    NormListResponse,
    NormResponse,
    NormUpdate,
    NormSyncResponse
)
from app.services.norm_service import NormService
from app.api.dependencies.auth import get_current_user
from app.models.user_model import User

router = APIRouter(
    prefix="/norms",
    tags=["Norms"],
)

@router.post(
    "/",
    response_model=NormResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_norm(
    data: NormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    norm = NormService.create(db, data)
    return {
        "success": True,
        "message": "Criado Norma com sucesso!",
        "data": norm,
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

@router.patch("/{norm_id}", response_model=NormResponse)
def update_norm(
    norm_id: int,
    data: NormUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    norm = NormService.update(db, norm_id, data)

    return {
        "success": True,
        "message": "Norma atualizada com sucesso!",
        "data": norm,
    }

@router.post("/sync",
             response_model=NormSyncResponse,
             dependencies=[Depends(get_current_user)],
)
def sync_norms(db: Session = Depends(get_db)):
    try:
        result = NormService.sync_from_scraper(db)

        return {
            "success": True,
            "message": "Sincronização concluída com sucesso!",
            "data": result,
        }

    # Indisponibilidade da Receita vira 503; uma resposta recebida com estrutura
    # inválida vira 502, pois o problema está no conteúdo do serviço externo.
    except FederalRevenueUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except FederalRevenueInvalidResponseError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
    
@router.delete("/{norm_id}", response_model=NormDeleteResponse)
def delete_norm(
    norm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    NormService.delete(db, norm_id)

    return {
        "success": True,
        "message": "Norma deletada com sucesso!",
    }
