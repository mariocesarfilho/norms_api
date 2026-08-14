from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    publication_date: str | None = Query(
        default=None,
        alias="date",
    ),
    search: str | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    data = DashboardService.get_dashboard(
        db=db,
        publication_date=publication_date,
        search=search,
    )

    return {
        "success": True,
        "message": "Dados do dashboard recuperados com sucesso",
        "data": data,
    }