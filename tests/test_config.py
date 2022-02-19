from kupy.config import *
from kupy.logger import logger


def test_properties_been_load():
    logger.info(type(default_setting))
    assert configs is not None
    assert configs.get("sqlalchemy_db_string").data != ""
    assert configs.get("log_level").data != ""
    assert configs.get("something_not_exists") is None
