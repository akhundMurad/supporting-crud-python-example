from redis import asyncio as aioredis
from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.business_logic.services.attendance_data_create_service import \
    AttendanceDataCreateService
from src.business_logic.services.attendance_report_load_service import \
    AttendanceReportLoadService
from src.data_access.persistence.postgresql.database_client import DatabaseClient
from src.data_access.cache.redis.cache_client import CacheClient
from src.config import CacheConfig, DatabaseConfig, LoggingConfig
from src.di.factories import (build_attendance_data_create_service,
                              build_attendance_report_load_service,
                              build_cache_client, build_cache_config,
                              build_database_client, build_database_config,
                              build_event_emitter, build_logging_config, build_redis_client,
                              build_sa_engine, build_sa_sessionmaker)
from src.presentation.consumer.event_emitter import EventEmitter

__all__ = ("get_container",)


def get_container() -> Container:
    container = Container()

    container.add_scoped_by_factory(build_database_config, DatabaseConfig)
    container.add_scoped_by_factory(build_cache_config, CacheConfig)
    container.add_scoped_by_factory(build_logging_config, LoggingConfig)
    container.add_scoped_by_factory(build_redis_client, aioredis.Redis)
    container.add_singleton_by_factory(build_sa_engine, AsyncEngine)
    container.add_scoped_by_factory(build_sa_sessionmaker, sessionmaker)
    container.add_scoped_by_factory(build_database_client, DatabaseClient)
    container.add_scoped_by_factory(build_cache_client, CacheClient)
    container.add_scoped_by_factory(
        build_attendance_data_create_service, AttendanceDataCreateService
    )
    container.add_scoped_by_factory(
        build_attendance_report_load_service, AttendanceReportLoadService
    )
    container.add_scoped_by_factory(build_event_emitter, EventEmitter)

    return container
