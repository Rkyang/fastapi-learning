from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import user
from config.db_config import get_db
from schemas.user import UserRequest

router = APIRouter()

@router.post("/register")
async def register(user_req: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await user.get_user_by_username(user_req.username, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    created_user = await user.create_user(user_req, db)

    token = await user.create_token(created_user.id, db)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": created_user.id,
                "username": created_user.username,
                "bio": created_user.bio,
                "avatar": created_user.avatar
            }
        }
    }
