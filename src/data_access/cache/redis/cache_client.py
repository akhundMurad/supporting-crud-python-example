from datetime import timedelta
from typing import AnyStr

from redis import asyncio as aioredis


class CacheClient:
    def __init__(self, redis: aioredis.Redis) -> None:
        self._redis = redis

    async def get(self, key: str) -> AnyStr | None:
        return await self._redis.get(key)

    async def put(self, key: str, value: AnyStr, ex: timedelta | None = None) -> None:
        await self._redis.set(key, value, ex)
