from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news_category

router = APIRouter()

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await news_category.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": result
    }