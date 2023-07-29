import unittest
from logging import Logger
from sys import stderr
from unittest.mock import MagicMock, patch

from loguru import logger
from opyoid import SingletonScope

from gpyt_eventbus.injection.modules.loguru_logger import LoguruModule
from gpyt_eventbus.interface.settings import Settings


class LoguruModuleTest(unittest.TestCase):
    def setUp(self):
        self.settings = MagicMock(spec=Settings)

    def test_get_logger(self):
        # Arrange
        module = LoguruModule()
        self.settings.log_level = "INFO"

        # Act
        with patch.object(logger, "remove") as mock_remove, patch.object(
            logger, "add"
        ) as mock_add:
            result = module.get_logger(self.settings)

        # Assert
        self.assertEqual(result, logger)
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(stderr, level="INFO")

    def test_configure(self):
        # Arrange
        module = LoguruModule()
        module.bind = MagicMock()

        module.configure()

        module.bind.assert_called_once_with(
            Logger, to_provider=module.get_logger, scope=SingletonScope
        )
