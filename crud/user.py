from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserRequest
from utils import security
from models.user import User


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