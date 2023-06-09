from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from data.db import get_async_session
from data.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from users.models import UserManager
from users.schemas import AuthUserModel, UuidTokenModel


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/auth/')
async def add_question(
        username: AuthUserModel,
        session: AsyncSession = Depends(get_async_session)
):
    """Авторизация пользователя"""
    async with session.begin():
        user_manager = UserManager(session)
        user = await user_manager.create_user(
            username=username.username
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return UuidTokenModel(
        uuid=user.uuid,
        token=access_token
    )
