from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

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

    @staticmethod
    def get_by_id(db: Session, norm_id: int) -> Norm | None:
        try:
            return db.get(Norm, norm_id)
        except SQLAlchemyError as error:
            print (f"Erro no banco de dados: {error}")
            raise

    @staticmethod
    def get_all(db: Session) -> list[Norm]:
        result = db.execute(select(Norm))

        return list(result.scalars().all())

    @staticmethod
    def update(db: Session, norm: Norm) -> Norm:
        try:
            db.commit()
            db.refresh(norm)

            return norm
        except SQLAlchemyError:
            db.rollback()
            raise