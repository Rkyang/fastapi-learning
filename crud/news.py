from sqlalchemy import select, func, update
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

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def add_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = (News.views + 1))
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_relate_news(db: AsyncSession, category_id: int, news_id: int):
    stmt = (select(News)
            .where(News.category_id == category_id, News.id != news_id)
            .order_by(News.views.desc(), News.publish_time.desc())
            .limit(5))
    r = await db.execute(stmt)
    # 使用列表推导式
    return [{
        "id": result.id,
        "title": result.title,
        "content": result.content,
        "image": result.image,
        "author": result.author,
        "publishTime": result.publish_time,
        "categoryId": result.category_id,
        "views": result.views,
    } for result in r.scalars().all()]