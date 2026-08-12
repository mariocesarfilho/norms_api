from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.norms import Norm

class NormRepository:

    @staticmethod
    async def find_all(db: AsyncSession, norm: Norm) -> list[Norm]:
        query = select(Norm)

        result = await db.execute(query)

        return result.scalars().all()