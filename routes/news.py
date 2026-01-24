from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news

router = APIRouter()

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": result
    }

@router.get("/list")
async def get_categories(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize"),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    result = await news.get_news_by_category_id(db, category_id, offset, page_size)

    total = await news.get_news_count_by_category_id(db, category_id)

    has_more = (offset + len(result)) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": result,
            "total": total,
            "hasMore": has_more
        }
    }