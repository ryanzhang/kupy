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


query_sql = "select * from fund"
expect_cache_file_path = (
    configs["data_folder"].data
    + "cache/"
    + DBAdaptor.get_hash_filename(query_sql)
    + ".parquet"
)


class TestDBAdaptor:
    @pytest.fixture(scope="class")
    def db(self):
        logger.info("Setup for Class")
        db = DBAdaptor(is_use_cache=True)
        db.execute_sql_file(
            os.path.dirname(os.path.abspath(__file__)) + "/init.sql"
        )
        if os.path.exists(expect_cache_file_path):
            os.remove(expect_cache_file_path)
        return db

    def test_delete_by_id_range(self, db: DBAdaptor):
        # Insert two records to fund
        entity_list = list()
        for i in range(5):
            fund = Fund()
            fund.ticker = "40000" + str(i)
            entity_list.append(fund)
        db.save_all(entity_list)

    def test_cache_file_name(self, db):
        cache1 = db.get_hash_filename("select * from fund")
        assert 5 == len(cache1)
        cache2 = db.get_hash_filename("select * from sync_status")
        assert 5 == len(cache2)
        assert cache1 != cache2

    def test_get_sql_without_cache(self, db):
        db.set_cache_mode(False)
        df = db.get_df_by_sql(query_sql)
        assert df is not None

    def test_get_sql_with_cache(self, db):
        db.set_cache_mode(True)
        df, csv_file = db.get_df_csv_by_sql(query_sql)
        assert df is not None
        assert csv_file is not None
        assert os.path.exists(expect_cache_file_path)
        assert os.path.exists(csv_file)

    def test_update_sync_status(self, db: DBAdaptor):
        # db.set_cache_mode(True)
        assert db.update_any_by_id(
            SyncStatus,
            1,
            {
                "rc": True,
                "update_time": datetime.datetime.now(),
                "comment": "更新前:55,增量:10",
            },
        )

    def test_load_sql(self, db):
        df_equ = db.get_df_by_sql(
            "select sec_id,ticker, sec_short_name from \
            fund"
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
        db.update_any_by_ticker(Fund, update_dict)
        df = db.get_df_by_sql(
            "select ticker, list_status_cd from fund where ticker in ('501216' ) "
        )
        logger.info(str(df))
        assert df.loc[df["list_status_cd"] != "L", :].shape[0] == 0

    def test_get_any_by_id(self, db: DBAdaptor):
        ss = db.get_any_by_id(SyncStatus, 1)
        assert ss is not None
        assert ss.table_name == "equity"
        assert ss.rc

    def test_execute_any_sql(self, db: DBAdaptor):
        db.execute_any_sql(
            "update sync_status set comment='update by test_execute_any_sql' where id =1 "
        )
        syncstatus = db.get_any_by_id(SyncStatus, 1)

        assert "update by test_execute_any_sql" == syncstatus.comment

    def test_get_any_by_any_column(self, db: DBAdaptor):
        ss = db.get_any_by_any_column(SyncStatus, "table_name", "equity")[0]
        # ss = db.get_any_by_id(SyncStatus, 1)
        assert ss is not None
        assert ss.table_name == "equity"
        assert ss.rc

    def test_execute_sql_file(self, db: DBAdaptor):
        test_sql_file = (
            os.path.dirname(os.path.abspath(__file__)) + "/test_sql_file.sql"
        )
        ret = db.execute_sql_file(test_sql_file)
        assert ret
