## 先创建一个数据库sandbox
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
        list_status_cd varchar(255),
        primary key (id)
    );

CREATE SEQUENCE IF NOT EXISTS kupy.fund_id_seq START WITH 1 INCREMENT BY 1;
CREATE UNIQUE INDEX IF NOT EXISTS fund_idx ON kupy.fund(sec_id);

INSERT INTO kupy.sync_status(id, table_name) VALUES(1, 'equity');

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
