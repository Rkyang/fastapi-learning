import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserRequest
from utils import security
from models.user import User, UserToken


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
