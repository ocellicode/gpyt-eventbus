from typing import Dict, List, Literal

from pydantic import BaseSettings, PyObject

from gpyt_eventbus.interface.settings import Settings as ICommandBusSettings
from gpyt_eventbus.resources.event import Event
from gpyt_eventbus.resources.subscriber import Subscriber

LogLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class StandardSettings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = [
        {"/subscriber": Subscriber},
        {"/event": Event},
    ]
    db_dsn: str = "sqlite:///gpyt_eventbus.db"
    db_echo: bool = True
    log_level: LogLevel = "INFO"

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
