from fastapi import HTTPException
from fastapi.params import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.user import get_user_by_token
from config.db_config import get_db


# 根据token查询用户，返回用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    # token = authorization.split(" ")[0]
    token = authorization
    user = await get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="身份无效，请重新登录")
    return user