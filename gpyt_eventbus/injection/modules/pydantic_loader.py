from typing import List

from pydantic import BaseSettings, PyObject

from .loguru_logger import LoguruModule
from .settings import SettingsModule


class PydanticLoader(BaseSettings):
    module_list: List[PyObject] = [
        SettingsModule,
        LoguruModule,
    ]

    class Config:
        env_prefix = "GPYT_"
