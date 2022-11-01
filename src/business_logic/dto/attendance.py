from datetime import date, datetime

from pydantic import UUID4, Field

from src.business_logic.dto import DTO


class CreateAttendance(DTO):
    external_id: UUID4 = Field(..., alias="attendance-id")
    student_id: UUID4 = Field(..., alias="new-student-id")
    lesson_id: UUID4 = Field(..., alias="new-lesson-id")
    participation_time: int = Field(..., alias="new-participation-time")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, alias="new-created-at"
    )

    class Config:
        allow_population_by_field_name = True


class LoadAttendanceReport(DTO):
    student_id: UUID4 = Field(...)
    start_date: date = Field(...)
    end_date: date = Field(...)


class ReadAttendanceReport(DTO):
    content: bytes = Field(...)
