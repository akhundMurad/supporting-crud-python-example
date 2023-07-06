from redis import asyncio as aioredis
from rodi import GetServiceContext
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.business_logic.dto.attendance import CreateAttendance
from src.business_logic.services.attendance_data_create_service import (
    AttendanceDataCreateService,
)
from src.business_logic.services.attendance_report_load_service import (
    AttendanceReportLoadService,
)
from src.config import CacheConfig, DatabaseConfig, LoggingConfig
from src.data_access.cache.redis.cache_client import CacheClient
from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.presentation.consumer.event_emitter import EventEmitter, Listener


def build_database_config(context: GetServiceContext) -> DatabaseConfig:
    return DatabaseConfig()


def build_cache_config(context: GetServiceContext) -> CacheConfig:
    return CacheConfig()


def build_logging_config(context: GetServiceContext) -> LoggingConfig:
    return LoggingConfig()


def build_redis_client(context: GetServiceContext) -> aioredis.Redis:
    config: CacheConfig = context.provider.get(CacheConfig)

    return aioredis.Redis.from_url(config.CACHE_CONNECTION_STRING)


def build_sa_engine(context: GetServiceContext) -> AsyncEngine:
    config: DatabaseConfig = context.provider.get(DatabaseConfig)

    return create_async_engine(config.DATABASE_CONNECTION_STRING)


def build_sa_sessionmaker(context: GetServiceContext) -> sessionmaker:
    engine = context.provider.get(AsyncEngine)

    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def build_database_client(context: GetServiceContext) -> DatabaseClient:
    session_factory = context.provider.get(sessionmaker)
    return DatabaseClient(session_factory=session_factory)


def build_cache_client(context: GetServiceContext) -> CacheClient:
    redis_client = context.provider.get(aioredis.Redis)
    return CacheClient(redis=redis_client)


def build_attendance_data_create_service(
    context: GetServiceContext,
) -> AttendanceDataCreateService:
    database_client = context.provider.get(DatabaseClient)

    return AttendanceDataCreateService(database_client=database_client)


def build_attendance_report_load_service(
    context: GetServiceContext,
) -> AttendanceReportLoadService:
    database_client = context.provider.get(DatabaseClient)
    cache_client = context.provider.get(CacheClient)

    return AttendanceReportLoadService(database_client=database_client, cache_client=cache_client)


def build_event_emitter(context: GetServiceContext) -> EventEmitter:
    ee = EventEmitter()
    ee.bind(
        event_type="attendance-created",
        listener=Listener(service_type=AttendanceDataCreateService, dto_type=CreateAttendance),
    )
    return ee
