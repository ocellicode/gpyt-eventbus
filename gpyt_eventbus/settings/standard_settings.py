from typing import Dict, List, Literal

from pydantic import BaseSettings, PyObject

from gpyt_eventbus.interface.settings import Settings as ICommandBusSettings

LogLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class StandardSettings(BaseSettings, ICommandBusSettings):
    resources: List[Dict[str, PyObject]] = []
    db_dsn: str = "sqlite:///gpyt_commandbus.db"
    db_echo: bool = True
    log_level: LogLevel = "INFO"

    class Config:
        env_prefix = "GPYT_"
        env_file = ".env"
