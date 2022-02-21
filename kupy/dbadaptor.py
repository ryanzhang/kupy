# -*- coding: UTF-8 -*-
import hashlib
import os.path
import traceback

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from kupy.config import configs
from kupy.logger import logger

_db_string = configs["sqlalchemy_db_string"].data

"""
DBAdaptor postgresql DB适配器
提供一下能力:
sql_query -> dataframe
sqlalchemy 增删改查 entity能力

"""


class DBAdaptor:
    def __init__(self, sqlalchemy_connect_string="", is_use_cache=False):
        """构造函数

        Args:
            conn_string (str, optional): psycogpg2库的数据库链接字符串. Defaults to 系统配置文件中的配置.
            sqlalchemy_connect_string(str, optional): sqlalchemy库的数据库链接串, Defaults to 系统配置文件中的配置.
            is_use_cache (bool, optional): 是否允许使用parquet cache对sql查询进行缓冲. Defaults to False.
        """

        self.is_use_cache = is_use_cache
        if sqlalchemy_connect_string == "":
            sqlalchemy_connect_string = _db_string
        logger.debug(
            f"sqlalchemy connection string: {sqlalchemy_connect_string}"
        )
        self.engine = create_engine(sqlalchemy_connect_string)

    def set_cache_mode(self, is_use_cache):
        """设置是否使用parquet cache缓存查询
        Args:
            is_use_cache (bool): True或者False, 会覆盖构造函数是的设定
        """
        self.is_use_cache = is_use_cache

    def get_df_csv_by_sql(self, query_sql: str) -> tuple[pd.DataFrame, str]:
        """get_df_by_sql一样，但是额外输出csv文件路径

        Args:
            query_sql ([str]): [sql query string]

        Returns:
            tuple[pd.DataFrame, str]: [返回两个参数，一个是DataFrame, 一个是输出csv路金]
        """
        df = self.get_df_by_sql(query_sql)
        csv_file_path = (
            configs["data_folder"].data
            + "cache/"
            + self.get_hash_filename(query_sql)
            + ".csv"
        )
        df.to_csv(csv_file_path)

        return df, csv_file_path

    def __get_df_by_sqlalchemy(self, query) -> pd.DataFrame:
        try:
            session = Session(self.engine)
            query = session.execute(query)
            df = pd.DataFrame(query.fetchall())
            if len(df) > 0:
                df.columns = query.keys()
            else:
                columns = query.keys()
                df = pd.DataFrame(columns=columns)
        except Exception as e:
            logger.error("执行{query}出错!")
            raise e
        return df

    def get_df_by_sql(self, query_sql: str) -> pd.DataFrame:
        """[根据sql返回DataFrame, 是否使用缓存保存parquet结果取决于set_cache_mode，或者构造函数设定]

        Args:
            query_sql ([str]): [sql查询语句]

        Returns:
            pd.DataFrame: [返回的dataframe]
        """
        if self.is_use_cache:
            df_cache_file = (
                configs["data_folder"].data
                + "cache/"
                + self.get_hash_filename(query_sql)
                + ".parquet"
            )
        else:
            df_cache_file = None

        if self.is_use_cache and os.path.exists(df_cache_file):
            df = pd.read_parquet(df_cache_file, engine="pyarrow")
        else:
            try:
                df = self.__get_df_by_sqlalchemy(query_sql)
            except Exception as e:
                logger.error(
                    "loading data from db failure" + traceback.format_exc()
                )
                logger.error("Exception is: " + str(e))
                df = None
            if df is None or df.shape[0] == 0:
                logger.warning(
                    "there is no data,pls check your query:" + query_sql
                )
            else:
                if self.is_use_cache:
                    logger.debug(
                        f"DF Size: {df.size}  Cache file: {df_cache_file} is_use_cache: {self.is_use_cache}"
                    )
                    df.to_parquet(df_cache_file, engine="pyarrow")

        return df

    def get_any_by_id(self, cls, id):
        """根据id号获取entity对象，返回的entity对象实例由cls 对象指定

        Args:
            cls (class对象): sqlalchemy的entity 对象
            id ([int]): [id的数字]

        Returns:
            [any]: [返回根据cls定义的对象实例, cls必须是sqlalchemy entity对象]
        """
        session = Session(self.engine)
        return session.query(cls).filter(cls.id == id)[0]

    def get_any_by_any_column(
        self, cls, column_name: str, column_value: str
    ) -> list:
        """根据id号获取entity对象，返回的entity对象实例由cls 对象指定

        Args:
            cls (class对象): sqlalchemy的entity 对象
            id ([int]): [id的数字]

        Returns:
            [any]: [返回根据cls定义的对象实例, cls必须是sqlalchemy entity对象]
        """
        session = Session(self.engine)
        table_name = ""
        if cls.__table__.schema is not None:
            table_name = cls.__table__.schema + "."
        table_name = cls.__table__.name

        return (
            session.query(cls)
            .from_statement(
                text(
                    f"select * from {table_name} where {column_name} = '{column_value}'"
                )
            )
            .all()
        )

    def save(self, entity) -> bool:
        """Save 单个sqlalchemy 对象

        Args:
            entity ([any sqlalchemy对象]): [必须是sqlalchemy 定义的实体对象]

        Returns:
            bool: [是否保存成功]
        """
        try:
            session = Session(self.engine)
            session.add(entity)
            session.commit()
        except Exception as e:
            logger.error("Save record to db error" + traceback.format_exc())
            logger.error("Exception is: " + str(e))
            return False

        return True

    def save_all(self, entitylist) -> bool:
        """保存多个实体对象列表

        Args:
            entitylist ([list]): [sqlalchemy entity object list]

        Returns:
            bool: [保存是否成功]
        """
        try:
            session = Session(self.engine)
            session.add_all(entitylist)
            session.commit()
        except Exception as e:
            logger.error("Save record to db error" + traceback.format_exc())
            logger.error("Exception is: " + str(e))
            return False

        return True

    # Ticker is the key in the update_dict
    def update_any_by_ticker(self, cls, update_dict: dict) -> bool:
        try:
            session = Session(self.engine)
            for key, value in update_dict.items():
                result = session.query(cls).filter(cls.ticker == key)
                if result is None:
                    logger.warning(f"{key} 不存在于{cls}表中，请检查！")
                    continue
                result.update(value)

            session.commit()
        except Exception as e:
            logger.error(
                "Update record to db {cls} error" + traceback.format_exc()
            )
            logger.error("Exception is: " + str(e))
            return False
        return True

    def update_any_by_id(self, cls, id, update_dict: dict) -> bool:
        """根据id以及 一个dict 来更新任意的sqlalchemy entitty表

        Args:
            id ([int]): entity的id号
            update_dict (dict): [需要更新的 dict对象，key:value单层结构]

        Returns:
            bool: [操作是否成功的结果]
        """
        try:
            session = Session(self.engine)
            result = session.query(cls).filter(cls.id == id)
            if result is None:
                logger.warning(f"{id} 不存在于{cls}表中，请检查！")
            result.update(update_dict)

            session.commit()
        except Exception as e:
            logger.error(
                "Update record to db {cls} error" + traceback.format_exc()
            )
            logger.error("Exception is: " + str(e))
            return False
        return True

    def delete_by_id(self, cls, id) -> bool:
        """Delete Any SqlAlchemy entity by Id

        Args:
            id ([int]): [entity id number]

        Returns:
            bool: [操作是否成功]
        """
        try:
            session = Session(self.engine)
            session.query(cls).filter(cls.id == id).delete()
            session.commit()
        except Exception as e:
            logger.error(
                "Delete record from db error" + traceback.format_exc()
            )
            logger.error("Exception is: " + str(e))
            return False

        return True

    def execute_any_sql(self, sql: str):
        try:
            # create a new cursor
            session = Session(self.engine)
            # execute the INSERT statement
            session.execute(sql)
            session.commit()
            logger.debug(f"Execute sql:{sql} successfully")
        except Exception as error:
            logger.error(f"Execute sql:{sql} error {error}")
            raise error

    def delete_all(self, cls) -> bool:
        """Delete all rows in SqlAlchemy entity

        Args:
            cls (class): [entity class name]

        Returns:
            bool: [操作是否成功]
        """
        logger.info("Underconstruction")
        return False
        pass
        # try:
        #     session = Session(self.engine)
        #     session.query(cls).all().delete()
        #     session.commit()
        # except Exception as e:
        #     logger.error(
        #         "Delete record from db error" + traceback.format_exc()
        #     )
        #     logger.error("Exception is: " + str(e))
        #     return False

        # return True

    def execute_sql_file(self, sql_file: str) -> bool:
        if not os.path.exists(sql_file):
            raise Exception(f"文件不存在: {sql_file}")
        try:
            session = Session(self.engine)
            sql = ""
            with open(sql_file, "rb") as f:
                lines = f.readlines()
                for bline in lines:
                    line = bline.decode("utf-8").strip()
                    if line.startswith("--"):
                        continue
                    if not line.endswith(";"):
                        sql = sql + line
                    else:
                        sql = sql + line
                        logger.debug(f"Execute sql: {sql}")
                        session.execute(sql)
                        sql = ""

            session.commit()
            logger.debug(f"Execute sql file:{sql_file} successfully")
        except Exception as error:
            logger.error(
                f"Execute sql:{sql_file}, sql statement:{sql} error {error}"
            )
            raise error
        return True

    @staticmethod
    def get_hash_filename(query_sql) -> str:
        """静态方法，根据sql生成5位hash串, 缓存parquet和csv文件以次命名, cache路径来自于configs["data_folder"].data设定+cache/目录

        Args:
            query_sql ([type]): [description]

        Returns:
            str: [description]
        """
        return hashlib.md5(query_sql.encode()).hexdigest()[0:5]
