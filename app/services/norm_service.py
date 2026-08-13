from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.norm_model import Norm
from app.repositories.norm_repository import NormRepository
from app.schemas.norm import NormCreate, NormUpdate

class NormService:
    @staticmethod
    def create(db: Session, data: NormCreate) -> Norm:
        norm = Norm(
            act_type=data.act_type,
            act_number=data.act_number,
            agency_unit=data.agency_unit,
            publication=data.publication,
            summary=data.summary
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

    @staticmethod
    def update(db: Session, norm_id: int, data: NormUpdate) -> Norm:
        norm = NormService.get_by_id(db, norm_id)

        if norm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Norma não encontrada",
            )

        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        for field, value in update_data.items():
            setattr(norm, field, value)

        return NormRepository.update(db, norm)

    @staticmethod
    def delete(db: Session, norm_id: int) -> None:
        norm = NormService.get_by_id(db, norm_id)

        if norm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Norma não encontrada",
        )

        NormRepository.delete(db, norm)
