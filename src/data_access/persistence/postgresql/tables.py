import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

metadata = sa.MetaData()


attendance_table = sa.Table(
    "attendance",
    metadata,
    sa.Column("attendance_id", sa.BigInteger, primary_key=True),
    sa.Column("external_id", UUID(as_uuid=True), unique=True),
    sa.Column("student_id", UUID(as_uuid=True), nullable=False),
    sa.Column("lesson_id", UUID(as_uuid=True), nullable=False),
    sa.Column("participation_time", sa.Integer, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False),
)
