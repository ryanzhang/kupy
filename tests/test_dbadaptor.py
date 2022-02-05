import datetime
import pytest
from kupy.dbadaptor import DBAdaptor
from kupy.logger import logger
from kupy.config import configs
import os

from tests.domain import Fund, SyncStatus

given = pytest.mark.parametrize
skipif = pytest.mark.skipif
skip = pytest.mark.skip
xfail = pytest.mark.xfail


query_sql = "select * from pyb.fund"
expect_cache_file_path = (
    configs["cache_folder"].data
    + DBAdaptor.calculateCacheFilename(query_sql)
    + ".pkl"
)


class TestDBAdaptor:
    @pytest.fixture(scope="class")
    def db(self):
        logger.info("Setup for Class")
        db = DBAdaptor(is_use_cache=True)
        if os.path.exists(expect_cache_file_path):
            os.remove(expect_cache_file_path)
        return db

    def test_cache_file_name(self, db):
        cache1 = db.calculateCacheFilename("select * from pyb.fund")
        assert 5 == len(cache1)
        cache2 = db.calculateCacheFilename("select * from pyb.sync_status")
        assert 5 == len(cache2)
        assert cache1 != cache2

    def test_get_sql_without_cache(self, db):
        db.setCacheMode(False)
        df, csv_file = db.getDfAndCsvBySql(query_sql)
        assert df is not None
        assert csv_file is not None
        # assert not os.path.exists(expect_cache_file_path)
        assert os.path.exists(csv_file)

    def test_get_sql_with_cache(self, db):
        db.setCacheMode(True)
        df, csv_file = db.getDfAndCsvBySql(query_sql)
        assert df is not None
        assert csv_file is not None
        assert os.path.exists(expect_cache_file_path)
        assert os.path.exists(csv_file)

    def test_update_sync_status(self, db:DBAdaptor):
        # db.setCacheMode(True)
        assert db.updateAnyeById(
            SyncStatus,
            1, {
                "rc":True,
                "update_time":datetime.datetime.now(),
                "comment":"更新前:55,增量:10"
            }
        )

    def test_load_sql(self, db):
        df_equ = db.getDfBySql(
            "select sec_id,ticker, sec_short_name from \
            pyb.fund"
        )
        assert df_equ is not None and df_equ.shape[0] > 0
        logger.info(f"stock account:{df_equ.shape[0]}")
        ticker = "000001"
        assert (
            df_equ.loc[df_equ.ticker == ticker, "sec_short_name"].iloc[0]
            == "平安基金"
        )

    def test_update_any_by_ticker(self):
        update_dict = {
            "501216": {"list_status_cd": "L"},
            "501216": {"list_status_cd": "L"},
        }
        db = DBAdaptor()
        db.updateAnyeByTicker(Fund, update_dict)
        df = db.getDfBySql(
            "select ticker, list_status_cd from pyb.fund where ticker in ('501216' ) "
        )
        logger.info(str(df))
        assert df.loc[df["list_status_cd"] != "L", :].shape[0] == 0

    def test_get_any_by_id(self, db:DBAdaptor):
        ss = db.getAnyById(SyncStatus, 1)
        assert ss is not None
        assert ss.table_name == "equity" 
        assert ss.rc

