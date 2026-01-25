from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import user
from config.db_config import get_db
from models.user import User
from schemas.user import UserRequest, UserAuthResponse, UserInfoBase, UserInfoResponse, PasswordChangeRequest
from utils.auth import get_current_user
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


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    result_user = await user.authenticate_user(db, user_data.username, user_data.password)
    if not result_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = await user.create_token(result_user.id, db)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(result_user))
    return success_response(message="登录成功", data=response_data)

@router.get("/info")
async def info(user_data: UserInfoResponse = Depends(get_current_user)):
    return success_response(data=UserInfoResponse.model_validate(user_data))

@router.put("/update")
async def update(
        user_upd: UserInfoBase,
        current_user: UserInfoResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_info = await user.update_user(db,user_upd, current_user.id)
    return success_response(data=UserInfoResponse.model_validate(user_info))

@router.put("/password")
async def update_password(
        pwd_upd: PasswordChangeRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await user.change_password(db,current_user, pwd_upd)
    if not result:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="failed to change password")
    return success_response()