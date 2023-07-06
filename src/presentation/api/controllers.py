from datetime import date
from uuid import UUID

from blacksheep import Response
from blacksheep.server.controllers import ApiController, get
from blacksheep.server.responses import file

from src.business_logic.dto.attendance import LoadAttendanceReport
from src.business_logic.services.attendance_report_load_service import (
    AttendanceReportLoadService,
)


class Attendance(ApiController):
    @get("/{student_id}/{start_date}/{end_date}")
    async def get_attendance_report(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date,
        service: AttendanceReportLoadService,
    ) -> Response:
        report = await service.execute(
            report_params=LoadAttendanceReport(student_id=student_id, start_date=start_date, end_date=end_date)
        )

        return file(
            report.content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
