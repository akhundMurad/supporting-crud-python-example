from blacksheep import Application

from src.data_access.cache.redis.cache_client import CacheClient


async def test_cache_client(asgi: Application) -> None:
    cache_client = asgi.service_provider.get(CacheClient)

    value = await cache_client.get("key")

    assert not value

    await cache_client.put("key", "value")

    value = await cache_client.get("key")

    assert value
    assert isinstance(value, bytes)
