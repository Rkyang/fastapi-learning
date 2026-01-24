from fastapi import APIRouter, HTTPException
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

@router.get("/detail")
async def get_news_detail(
        new_id: int = Query(..., alias="id"),
        db: AsyncSession = Depends(get_db)
):
    # 查询详情
    result = await news.get_news_detail(db, new_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")

    # 增加浏览量
    await news.add_views(db, new_id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": result.id,
            "title": result.title,
            "content": result.content,
            "image": result.image,
            "author": result.author,
            "publishTime": result.publish_time,
            "categoryId": result.category_id,
            "views": result.views,
            "relatedNews": []
        }
    }