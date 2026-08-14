from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select, String, cast, or_, select

from app.models.norm_model import Norm

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

    @staticmethod
    def delete(db: Session, norm: Norm) -> None:
        try:
            db.delete(norm)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def get_by_source_id(
        db: Session, source_id: int
    ) -> Norm | None:
        result = db.execute(
            select(Norm).where(
                Norm.source_id == source_id
                )
        )

        return result.scalar_one_or_none()

    @staticmethod
    def get_dashboard_data(
        db: Session,
        publication: str | None = None,
        search: str | None = None
    ) -> list[Norm]:
        """Combina filtros opcionais de publicação exata e busca parcial.

        A busca inclui tipo, órgão, resumo e o número do ato convertido em texto.
        """
        statement = select(Norm)

        if publication is not None:
            statement = statement.where(
                Norm.publication == publication
            )

        if search:
            search_term = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    Norm.act_type.ilike(search_term),
                    Norm.agency_unit.ilike(search_term),
                    Norm.summary.ilike(search_term),
                    cast(Norm.act_number, String).ilike(search_term),
                )
            )

        result = db.execute(statement)

        return list(result.scalars().all())
