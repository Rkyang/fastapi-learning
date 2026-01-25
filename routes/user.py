from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import user
from config.db_config import get_db
from schemas.user import UserRequest, UserAuthResponse, UserInfoBase, UserInfoResponse
from utils.response import success_response

router = APIRouter()

@router.post("/register")
async def register(user_req: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await user.get_user_by_username(user_req.username, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    created_user = await user.create_user(user_req, db)

    token = await user.create_token(created_user.id, db)

    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(created_user))

    return success_response(message="注册成功", data=response_data)
