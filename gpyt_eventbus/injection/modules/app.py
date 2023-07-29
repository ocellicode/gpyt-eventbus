from logging import Logger

from flask import Flask
from flask_restful import Api
from opyoid import Module, SingletonScope
from sqlalchemy.orm import Session

from gpyt_eventbus.interface.settings import Settings


class AppModule(Module):
    @staticmethod
    def get_app(settings: Settings, logger: Logger, session: Session) -> Flask:
        app = Flask(__name__)
        api = Api(app)
        for res in settings.resources:
            for key, value in res.items():
                api.add_resource(
                    value,
                    key,
                    resource_class_kwargs={
                        "logger": logger,
                        "session": session,
                    },
                )

        return app

    def configure(self) -> None:
        self.bind(Flask, to_provider=self.get_app, scope=SingletonScope)
