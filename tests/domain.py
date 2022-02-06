from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    Sequence,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SyncStatus(Base):
    __tablename__ = "sync_status"
    __table_args__ = {"schema": "pyb"}

    id = Column(
        Integer,
        primary_key=True,
    )
    rc = Column(Boolean)
    table_name = Column(String(64))  #     证券交易所
    update_time = Column(DateTime)  #     日期
    comment = Column(String(255))  # 更新说明

    def __init__(self):
        pass


# 不完整字段
class Fund(Base):
    __tablename__ = "fund"
    __table_args__ = {"schema": "pyb"}

    id = Column(
        Integer, Sequence("fund_id_seq", schema="pyb"), primary_key=True
    )
    sec_id = Column(
        String(255)
    )  # secID; //    通联编制的证券编码，可使用DataAPI.SecIDGet获取
    ticker = Column(String(255))  # ticker; //    通用交易代码
    sec_short_name = Column(String(255))  # secShortName; //    证券简称
    category = Column(String(255))
    operation_mode = Column(String(255))
    index_fund = Column(String(255))
    etf_lof = Column(String(255))
    is_qdii = Column(String(255))
    is_fof = Column(String(255))
    exchange_cd = Column(String(255))
    list_status_cd = Column(String(255))
    list_date = Column(DateTime)
    delist_date = Column(DateTime)
    idx_id = Column(String(255))
    idx_ticker = Column(String(255))
    idx_short_name = Column(String(255))

    def __init__(self):
        pass
