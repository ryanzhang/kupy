import pytest

from kupy import BaseClass, base_function
from kupy.logger import logger
from kupy.config import configs

given = pytest.mark.parametrize


@given("fn", [BaseClass(), base_function])
def test_parameterized(fn):
    assert "hello from" in fn()


def test_base_function():
    assert base_function() == "hello from base function"


def test_base_class():
    assert BaseClass().base_method() == "hello from BaseClass"


def test_find_package_name():
    logger.info(__name__)
    pass
    # assert "kupy" =
