# 先创建一个数据库sandbox
创建表
```
create schema kupy;
CREATE TABLE IF NOT EXISTS kupy.sync_status  (
    id BIGINT NOT NULL,
    table_name VARCHAR(255),
    rc boolean,
    update_time TIMESTAMP,
    comment VARCHAR(255),
    PRIMARY KEY (id)
);
create table kupy.fund (
       id bigint not null,
        sec_id varchar(255),
        ticker varchar(255),
        sec_short_name varchar(255),
        trade_abbr_name varchar(255),
        category varchar(255),
        operation_mode varchar(255),
        index_fund varchar(255),
        etf_lof varchar(255),
        is_qdii boolean,
        is_fof boolean,
        is_guar_fund boolean,
        guar_period float,
        guar_ratio float,
        exchange_cd varchar(255),
        list_status_cd varchar(255),
        manager_name varchar(255),
        status varchar(255),
        establish_date date,
        list_date date,
        delist_date date,
        expire_date date,
        management_company integer,
        management_full_name varchar(255),
        custodian integer,
        custodian_full_name varchar(255),
        invest_field varchar(3072),
        invest_target varchar(2048),
        perf_benchmark varchar(255),
        circulation_shares float,
        is_class integer,
        idx_id varchar(255),
        idx_ticker varchar(255),
        idx_short_name varchar(255),
        management_short_name varchar(255),
        custodian_short_name varchar(255),
        sec_full_name varchar(255),
        class_name varchar(255),
        primary key (id)
    );

CREATE SEQUENCE IF NOT EXISTS kupy.fund_id_seq START WITH 1 INCREMENT BY 1;
CREATE UNIQUE INDEX IF NOT EXISTS fund_idx ON kupy.fund(sec_id);

INSERT INTO kupy.sync_status(id, table_name) VALUES(1, 'equity');
INSERT INTO kupy.sync_status(id, table_name) VALUES(2, 'equity_industry');
INSERT INTO kupy.sync_status(id, table_name) VALUES(3, 'equ_share');
INSERT INTO kupy.sync_status(id, table_name) VALUES(4, 'fund');
INSERT INTO kupy.sync_status(id, table_name) VALUES(5, 'fund_day');
INSERT INTO kupy.sync_status(id, table_name) VALUES(6, 'idx');
INSERT INTO kupy.sync_status(id, table_name) VALUES(7, 'mkt_equ_day');
INSERT INTO kupy.sync_status(id, table_name) VALUES(8, 'mkt_idx_day');
INSERT INTO kupy.sync_status(id, table_name) VALUES(9, 'trade_calendar');

insert into kupy.fund(id, sec_id, ticker, sec_short_
 name, list_status_cd) values(1, '000001.XSHE', '000001', '
 平安基金', 'L');
insert into kupy.fund(id, sec_id, ticker, sec_short_
 name, list_status_cd) values(2, '501216.XSHE', '501216', '
 测试基金', 'UN');
```

Grant permission on user
```
GRANT CONNECT ON DATABASE sandbox TO "user";
GRANT USAGE ON SCHEMA kupy TO "user";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA kupy TO "user";

```
