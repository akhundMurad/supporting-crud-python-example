import asyncio

import pytest
from typing import AsyncIterator
from redis import asyncio as aioredis
from blacksheep import Application
from blacksheep.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine

from src.data_access.persistence.postgresql.tables import metadata
from src.presentation.api.asgi import asgi as asgi_application


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def asgi() -> AsyncIterator[Application]:
    await asgi_application.start()
    yield asgi_application
    await asgi_application.stop()


@pytest.fixture(autouse=True)
async def migration(asgi: Application) -> AsyncIterator[None]:
    engine = asgi.service_provider.get(AsyncEngine)
    redis = asgi.service_provider.get(aioredis.Redis)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    await redis.flushdb()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def test_client(asgi: Application) -> TestClient:
    return TestClient(asgi)
