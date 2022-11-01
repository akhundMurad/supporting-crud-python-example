import logging

from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from rodi import Services

from src.config import LoggingConfig
from src.di.container import get_container
from src.presentation.api.controllers import Attendance  # noqa


def build_asgi_application():
    app = Application(services=get_container())

    setup_logging(app.services.build_provider())

    docs = OpenAPIHandler(info=Info(title="Attendance Reporter API", version="0.0.1"))
    docs.bind_app(app)

    return app


def setup_logging(provider: Services) -> None:
    settings = provider.get(LoggingConfig)
    logging.basicConfig(level=settings.LOG_LEVEL)


asgi = build_asgi_application()
