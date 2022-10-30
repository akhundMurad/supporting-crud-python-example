from io import BytesIO

import xlsxwriter as excel
from src.business_logic.dto.attendance import LoadAttendanceReport, ReadAttendanceReport

from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.data_access.cache.redis.cache_client import CacheClient
from src.data_access.persistence.postgresql.tables import attendance_table


class AttendanceReportLoadService:
    def __init__(
        self, database_client: DatabaseClient, cache_client: CacheClient
    ) -> None:
        self._db = database_client
        self._cache_client = cache_client

    async def execute(
        self, report_params: LoadAttendanceReport
    ) -> ReadAttendanceReport:
        async with self._db as db:
            excel_document = await self._cache_client.get(
                f"attendance_report_{report_params.student_id}_{report_params.start_date}_{report_params.end_date}"
            )
            if not excel_document:
                statement = f"""
                SELECT * FROM {attendance_table.name} 
                WHERE student_id = :student_id AND created_at BETWEEN :start_date AND :end_date
                """
                attendance_list = list(
                    await db.execute(
                        statement,
                        student_id=report_params.student_id,
                        start_date=report_params.start_date,
                        end_date=report_params.end_date,
                    )
                )

                excel_document = _generate_excel_document(attendance_list)

            await db.commit()

        return ReadAttendanceReport(content=excel_document)


def _generate_excel_document(attendance_list: list) -> bytes:
    output = BytesIO()
    workbook = excel.Workbook(output)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for attendance in attendance_list:
        worksheet.write(row, col, attendance[0])
        worksheet.write(row, col + 1, attendance[1])
        worksheet.write(row, col + 2, attendance[2])
        worksheet.write(row, col + 3, attendance[3])
        worksheet.write(row, col + 4, attendance[4])
        row += 1

    workbook.close()

    return output.getvalue()
