from typing import List

from pydantic import BaseSettings, PyObject

from .app import AppModule
from .engine import EngineModule
from .loguru_logger import LoguruModule
from .session import SessionModule
from .settings import SettingsModule


class PydanticLoader(BaseSettings):
    module_list: List[PyObject] = [
        SettingsModule,
        LoguruModule,
        EngineModule,
        SessionModule,
        AppModule,
    ]

    class Config:
        env_prefix = "GPYT_"
