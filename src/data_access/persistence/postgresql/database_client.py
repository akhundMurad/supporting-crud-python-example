import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseClient:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "DatabaseClient":
        self._session: AsyncSession = self._session_factory()  # type: ignore
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            logging.error(f"Handled exception: {exc_type.__name__} - {exc_val}")
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def execute(self, statement: str, **params) -> Any:
        return await self._session.execute(text(statement), params)
