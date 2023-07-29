from sqlite3 import Connection as SQLite3Connection

from opyoid import Module, SingletonScope
from sqlalchemy import event
from sqlalchemy.engine import Engine, create_engine

from gpyt_eventbus.interface.settings import Settings


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(
    dbapi_connection, connection_record
):  # pylint: disable=unused-argument
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class EngineModule(Module):
    @staticmethod
    def get_engine(settings: Settings) -> Engine:
        return create_engine(settings.db_dsn, echo=settings.db_echo)

    def configure(self) -> None:
        self.bind(Engine, to_provider=self.get_engine, scope=SingletonScope)
