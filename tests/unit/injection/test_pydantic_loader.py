import math
import unittest

from hamcrest import *

from gpyt_eventbus.injection.modules.pydantic_loader import PydanticLoader


class TestPydanticLoader(unittest.TestCase):
    def test_configure(self):
        pydantic_loader = PydanticLoader()

        assert isinstance(pydantic_loader.module_list, list)
        assert len(pydantic_loader.module_list) == 3
        assert_that(pydantic_loader.module_list, is_([math.cos, math.sin, math.tan]))
