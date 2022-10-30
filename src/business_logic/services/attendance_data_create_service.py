from src.business_logic.dto.attendance import CreateAttendance

from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.data_access.persistence.postgresql.tables import attendance_table


class AttendanceDataCreateService:
    def __init__(self, database_client: DatabaseClient) -> None:
        self._db = database_client

    async def execute(self, attendance: CreateAttendance) -> None:
        async with self._db as db:
            statement = f"""
            INSERT INTO {attendance_table.name}(external_id, student_id, lesson_id, participation_time, created_at) 
            VALUES(:external_id, :student_id, :lesson_id, :participation_time, :created_at)
            """
            await db.execute(
                statement,
                external_id=attendance.external_id,
                student_id=attendance.student_id,
                lesson_id=attendance.lesson_id,
                participation_time=attendance.participation_time,
                created_at=attendance.created_at,
            )
            await db.commit()
