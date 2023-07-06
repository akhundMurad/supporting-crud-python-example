import uuid
from datetime import datetime

from blacksheep import Application

from src.business_logic.dto.attendance import CreateAttendance
from src.business_logic.services.attendance_data_create_service import (
    AttendanceDataCreateService,
)
from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.data_access.persistence.postgresql.tables import attendance_table


async def test_attendance_creation(asgi: Application):
    service = asgi.service_provider.get(AttendanceDataCreateService)
    database_client = asgi.service_provider.get(DatabaseClient)

    new_attendace = {
        "attendance-id": str(uuid.uuid4()),
        "new-external-id": str(uuid.uuid4()),
        "new-student-id": str(uuid.uuid4()),
        "new-lesson-id": str(uuid.uuid4()),
        "new-participation-time": 3723,
        "new-created-at": str(datetime.now()),
    }

    await service.execute(attendance=CreateAttendance(**new_attendace))

    async with database_client as db:
        attendances = list(await db.execute(f"""SELECT * FROM {attendance_table.name}"""))
        assert len(attendances) == 1
