import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserRequest, UserInfoBase
from utils import security
from models.user import User, UserToken

async def get_user_by_id(user_id: int, db: AsyncSession):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_username(username: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(user_data: UserRequest, db: AsyncSession):
    hashed_pwd = security.get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_token(user_id: int, db: AsyncSession):
    # token值
    token = str(uuid.uuid4())
    # 过期时间
    expired_at = datetime.now() + timedelta(days=7)

    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    token_info = result.scalar_one_or_none()
    if token_info:
        token_info.token = token
        token_info.expires_at = expired_at
    else:
        token_info = UserToken(user_id=user_id, token=token, expires_at=expired_at)
        db.add(token_info)
    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(username, db)
    if not user:
        return None
    if not security.validate_password(password, user.password):
        return None
    return user

async def get_user_by_token(token: str, db: AsyncSession):
    token_query = select(UserToken).where(UserToken.token == token)
    result_token = await db.execute(token_query)
    token_info = result_token.scalar_one_or_none()
    if not token_info or token_info.expires_at < datetime.now():
        return None
    user_query = select(User).where(User.id == token_info.user_id)
    result_user = await db.execute(user_query)
    user_info = result_user.scalar_one_or_none()
    if not user_info:
        return None
    return user_info

async def update_user(
        db: AsyncSession,
        user_upd: UserInfoBase,
        user_id: int
):
    smst = update(User).where(User.id == user_id).values(
        # 没有设置值的不更新
        **user_upd.model_dump(
            exclude_unset=True,
            exclude_none=True
        )
    )
    result = await db.execute(smst)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user_info = await get_user_by_id(user_id, db)
    return user_info

