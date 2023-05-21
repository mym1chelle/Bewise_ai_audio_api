import uuid
from fastapi import Depends, status
from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy import Column, DateTime, UUID, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
import datetime
from data.db import Base, async_session_maker
from data.auth import SECRET_KEY, ALGORITHM
from users.schemas import TokenDataModel


class User(Base):
    __tablename__ = 'users'

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    username = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UserManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, uuid: str):
        try:
            query = select(User).where(User.uuid == uuid)
            result = await self.session.execute(query)
        except DBAPIError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Token entry error',
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = result.scalars().first()
        if user:
            return user
        return None

    async def create_user(self, username: str):
        new_user = User(
            username=username
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def get_current_user(self, token: str, uuid: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            print(username)
            if username is None:
                raise credentials_exception
            token_data = TokenDataModel(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user(uuid=uuid)
        print(user)
        if not user or user.username != token_data.username:
            raise credentials_exception
        return user
