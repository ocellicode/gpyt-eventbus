from abc import ABC
from typing import Any, Callable, Dict, List


class Settings(ABC):
    resources: List[Dict[str, Callable[..., Any]]]
    db_dsn: str
    db_echo: bool
    log_level: str
