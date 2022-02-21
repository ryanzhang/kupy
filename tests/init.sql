drop table IF EXISTS sync_status;
drop table IF EXISTS fund;
CREATE TABLE IF NOT EXISTS sync_status  (
    id BIGINT NOT NULL,
    table_name VARCHAR(255),
    rc boolean,
    update_time TIMESTAMP,
    comment VARCHAR(255),
    PRIMARY KEY (id)
);
create table fund (
       id bigint not null,
        sec_id varchar(255),
        ticker varchar(255),
        sec_short_name varchar(255),
        list_status_cd varchar(255),
        primary key (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS fund_idx ON fund(sec_id);
INSERT INTO sync_status(id, table_name,rc,comment) VALUES(1, 'equity',True, 'initial update');

insert into fund(id, sec_id, ticker, sec_short_
 name, list_status_cd) values(1, '000001.XSHE', '000001', '
 平安基金', 'L');
insert into fund(id, sec_id, ticker, sec_short_
 name, list_status_cd) values(2, '501216.XSHE', '501216', '
 测试基金', 'UN');
