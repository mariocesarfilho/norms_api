from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.norms_model import Norm

class NormRepository:
    @staticmethod
    def create(db: Session, norm: Norm) -> Norm:
        try:
            db.add(norm)
            db.commit()
            db.refresh(norm)

            return norm
        except SQLAlchemyError:
            db.rollback()
            raise