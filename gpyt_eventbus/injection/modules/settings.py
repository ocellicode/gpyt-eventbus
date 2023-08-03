from opyoid import Module, SingletonScope

from gpyt_eventbus.interface.settings import Settings as ISettings
from gpyt_eventbus.settings import StandardSettings


class SettingsModule(Module):
    def configure(self) -> None:
        self.bind(ISettings, to_class=StandardSettings, scope=SingletonScope)
