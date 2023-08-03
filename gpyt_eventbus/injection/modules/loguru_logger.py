from logging import Logger
from sys import stderr

from loguru import logger
from opyoid import Module, SingletonScope

from gpyt_eventbus.interface.settings import Settings


class LoguruModule(Module):
    @staticmethod
    def get_logger(settings: Settings) -> Logger:
        logger.remove()
        logger.add(stderr, level=settings.log_level)
        return logger  # type: ignore

    def configure(self) -> None:
        self.bind(Logger, to_provider=self.get_logger, scope=SingletonScope)
