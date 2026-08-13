from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.norms_model import Norm
from app.repositories.norm_repository import NormRepository
from app.schemas.norm import NormCreate

class NormService:
    @staticmethod
    def create(db: Session, data: NormCreate) -> Norm:
        norm = Norm(
            act_type = data.act_type,
            act_number = data.act_number,
            agency_unit = data.agency_unit,
            publication = data.publication,
            summary = data.summary
        )

        return NormRepository.create(db, norm)

    @staticmethod
    def get_by_id(db: Session, norm_id: int) -> Norm:
        norm = NormRepository.get_by_id(db, norm_id)

        if norm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Norma não encontrada"
            )

        return norm

    @staticmethod
    def get_all(db: Session) -> list[Norm]:
        return NormRepository.get_all(db)