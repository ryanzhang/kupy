-- This is a comments
CREATE TABLE IF NOT EXISTS sync_status  (
    id BIGINT NOT NULL,
    table_name VARCHAR(255),
    rc boolean,
    update_time TIMESTAMP,
    comment VARCHAR(255),
    PRIMARY KEY (id)
);
create table if not exists fund (
       id bigint not null,
        sec_id varchar(255),
        ticker varchar(255),
        sec_short_name varchar(255),
        list_status_cd varchar(255),
        primary key (id)
);
