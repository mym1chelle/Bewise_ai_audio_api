import asyncio

from httpx import AsyncClient
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest
from pathlib import Path
import sys

path = Path(__file__).resolve().parent.parent
sys.path.append(str(path) + '/')

from main import app
from data.db import get_async_session, Base
from data.config import load_config

config = load_config()

SQLALCHEMY_TEST_DATABASE_URL = config.test.uri

engine_test = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)
async_session_maker_test = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def create_db():
    async with engine_test.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
