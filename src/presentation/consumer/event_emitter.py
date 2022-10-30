import logging
from typing import Type, TypedDict

from rodi import Services

from src.business_logic.dto import DTO


class Listener(TypedDict):
    service_type: Type
    dto_type: Type[DTO]



class EventEmitter:
    def __init__(self) -> None:
        self._mapping: dict[str, list[Listener]] = {}

    def bind(self, *, event_type: str, listener: Listener) -> None:
        listeners = self._mapping.get(event_type, [])
        listeners.append(listener)
        self._mapping[event_type] = listeners

    async def emit(self, *, message: dict, provider: Services) -> None:
        event_name = message.get("type", "")
        listeners = self._mapping.get(event_name, [])
        for listener in listeners:
            service_type = listener["service_type"]
            dto_type = listener["dto_type"]
            
            service = provider.get(service_type)
            logging.debug(
                f"Handling event named {event_name} by service {service_type.__name__}."
            )
            await service.execute(dto_type(**message["payload"]))
