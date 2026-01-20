from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.news_category import NewsCategory


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(NewsCategory).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()