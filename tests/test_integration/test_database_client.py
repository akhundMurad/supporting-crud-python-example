import uuid
from datetime import datetime

import pytest
from blacksheep import Application

from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.data_access.persistence.postgresql.tables import attendance_table


async def test_database_client_rollback(asgi: Application) -> None:
    class SomeException(Exception):
        ...

    database_client = asgi.service_provider.get(DatabaseClient)

    with pytest.raises(SomeException):
        async with database_client as db:
            await db.execute(
                f"""
                INSERT INTO {attendance_table.name}(external_id, student_id, lesson_id, participation_time, created_at)
                VALUES(:external_id, :student_id, :lesson_id, :participation_time, :created_at)
                """,
                **dict(
                    external_id=uuid.uuid4(),
                    student_id=uuid.uuid4(),
                    lesson_id=uuid.uuid4(),
                    participation_time=3600,
                    created_at=datetime.now(),
                ),
            )

            raise SomeException()

            await db.commit()

    async with database_client as db:
        assert not list(await db.execute(f"SELECT * FROM {attendance_table.name}"))


async def test_database_client_without_commit(asgi: Application) -> None:
    database_client = asgi.service_provider.get(DatabaseClient)

    async with database_client as db:
        await db.execute(
            f"""
            INSERT INTO {attendance_table.name}(external_id, student_id, lesson_id, participation_time, created_at)
            VALUES(:external_id, :student_id, :lesson_id, :participation_time, :created_at)
            """,
            **dict(
                external_id=uuid.uuid4(),
                student_id=uuid.uuid4(),
                lesson_id=uuid.uuid4(),
                participation_time=3600,
                created_at=datetime.now(),
            ),
        )

    async with database_client as db:
        assert not list(await db.execute(f"SELECT * FROM {attendance_table.name}"))


async def test_database_client_commit(asgi: Application) -> None:
    database_client = asgi.service_provider.get(DatabaseClient)

    async with database_client as db:
        await db.execute(
            f"""
            INSERT INTO {attendance_table.name}(external_id, student_id, lesson_id, participation_time, created_at)
            VALUES(:external_id, :student_id, :lesson_id, :participation_time, :created_at)
            """,
            **dict(
                external_id=uuid.uuid4(),
                student_id=uuid.uuid4(),
                lesson_id=uuid.uuid4(),
                participation_time=3600,
                created_at=datetime.now(),
            ),
        )

        await db.commit()

    async with database_client as db:
        assert list(await db.execute(f"SELECT * FROM {attendance_table.name}"))
