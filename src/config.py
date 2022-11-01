from enum import Enum

from pydantic import BaseSettings


class LoggingLevelEnum(int, Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10


class DatabaseConfig(BaseSettings):
    DATABASE_CONNECTION_STRING: str


class CacheConfig(BaseSettings):
    CACHE_CONNECTION_STRING: str


class LoggingConfig(BaseSettings):
    LOG_LEVEL: LoggingLevelEnum = LoggingLevelEnum.INFO
