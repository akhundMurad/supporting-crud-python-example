import asyncio
import json
import logging

from redis import asyncio as aioredis
from rodi import Services
from src.config import LoggingConfig

from src.di.container import get_container
from src.presentation.consumer.event_emitter import EventEmitter


async def consume() -> None:
    container = get_container()
    provider = container.build_provider()

    setup_logging(provider)

    logging.info("Redis event consumer has been started.")

    redis = provider.get(aioredis.Redis)
    message_handler = provider.get(EventEmitter)

    pubsub = redis.pubsub(ignore_subscribe_messages=True)
    await pubsub.subscribe("attendance")

    async for message in await pubsub.listen():
        message: dict = json.loads(message["data"])
        try:
            await message_handler.emit(message=message, provider=provider)
        except Exception as ex:
            logging.error(ex)


def setup_logging(provider: Services) -> None:
    settings = provider.get(LoggingConfig)
    logging.basicConfig(level=settings.LOG_LEVEL)


if __name__ == "__main__":
    asyncio.run(consume())
