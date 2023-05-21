from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from data.db import get_async_session
from data.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List
from users.models import User, UserManager
from users.schemas import AuthUserModel


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/auth')
async def add_question(
        username: AuthUserModel,
        session: AsyncSession = Depends(get_async_session)
):
    """Авторизация пользователя"""
    print(username.username)
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
    return {
        'uuid': user.uuid,
        'acess_token': f'Bearer {access_token}'
    }


@router.get("/me/")
async def read_users_me(
    token: str,
    uuid: str,
    session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        user_manager = UserManager(session)
    return await user_manager.get_current_user(
        token=token,
        uuid=uuid
    )
