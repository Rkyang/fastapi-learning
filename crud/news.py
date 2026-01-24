from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import NewsCategory, News

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(NewsCategory).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_by_category_id(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 100):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count_by_category_id(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()