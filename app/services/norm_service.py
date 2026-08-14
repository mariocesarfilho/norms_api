from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.norm_model import Norm
from app.repositories.norm_repository import NormRepository
from app.schemas.norm import NormCreate, NormUpdate
from app.scrapers.federal_revenue_scraper import scrape_norms

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

    @staticmethod
    def sync_from_scraper(
        db: Session
    ) -> dict:
        scraped_norms = scrape_norms()

        created = 0
        skipped = 0

        for data in scraped_norms:
            source_id = data["source_id"]

            if source_id is None:
                skipped += 1
                continue

            existing_norm = NormRepository.get_by_source_id(
                db, 
                source_id
            )

            if existing_norm is not None:
                skipped += 1
                continue

            norm = Norm(
                source_id=source_id,
                act_type=data["act_type"],
                act_number=data["act_number"],
                agency_unit=data["agency_unit"],
                publication=data["publication"],
                summary=data["summary"]
            )

            NormRepository.create(db, norm)
            created += 1

        return {
            "found": len(scraped_norms),
            "created": created,
            "skipped": skipped
        }
