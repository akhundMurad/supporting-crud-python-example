from datetime import date
from io import BytesIO
from uuid import uuid4

import openpyxl
from blacksheep import Application
from blacksheep.testing import TestClient


async def test_attendance_report_without_data(
    asgi: Application, test_client: TestClient
) -> None:
    student_id = uuid4()
    start_date = date(2022, 10, 10)
    end_date = date(2022, 10, 10)

    response = await test_client.get(
        f"/api/attendance/{student_id}/{start_date}/{end_date}"
    )

    assert response.status == 200
    assert response.content.length

    io = BytesIO(await response.content.read())
    workbook = openpyxl.load_workbook(io, read_only=True)
    workbook = workbook.active

    assert not list(workbook.rows)
