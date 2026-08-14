from collections import Counter
from datetime import datetime
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.repositories.norm_repository import NormRepository

class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        publication_date: datetime | None = None,
        search: str | None = None,
    ) -> dict:

        publication = None

        if publication_date is not None:
            try:
                datetime.strptime(
                publication_date,
                "%d/%m/%Y"
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="A data deve estar no formato DD/MM/YYYY",
                )

        norms = NormRepository.get_dashboard_data(
            db=db,
            publication=publication_date,
            search=search,
        )

        act_types = Counter(
            norm.act_type
            for norm in norms
        )

        agencies = Counter(
            norm.agency_unit
            for norm in norms
        )

        return {
            "total_norms": len(norms),
            "total_act_types": len(act_types),
            "total_agencies": len(agencies),

            "by_act_type": [
                {
                    "act_type": act_type,
                    "total": total,
                }
                for act_type, total in act_types.items()
            ],

            "by_agency": [
                {
                    "agency_unit": agency,
                    "total": total,
                }
                for agency, total in agencies.items()
            ],

            "norms": norms,
        }