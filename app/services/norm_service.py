from sqlalchemy.orm import Session

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