"""Use opyoid to create sqlalchemy session"""

from opyoid import Module, SingletonScope
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class SessionModule(Module):
    """Use opyoid to create sqlalchemy session"""

    @staticmethod
    def get_session(engine: Engine) -> Session:
        """Use opyoid to create sqlalchemy session"""
        return sessionmaker(bind=engine)()

    def configure(self) -> None:
        """Use opyoid to create sqlalchemy session"""
        self.bind(Session, to_provider=self.get_session, scope=SingletonScope)
