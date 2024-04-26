DROP TABLE cdm.user_category_counters;
CREATE TABLE cdm.user_category_counters (
	id serial4 NOT NULL PRIMARY KEY,
	user_id uuid NOT NULL,
	category_id uuid NOT NULL,
	category_name varchar NOT NULL,
	order_cnt int4 NOT NULL CHECK ((order_cnt >= 0))
);

DROP TABLE cdm.user_product_counters;
CREATE TABLE cdm.user_product_counters (
	id serial4 NOT NULL PRIMARY KEY ,
	user_id uuid NOT NULL,
	product_id uuid NOT NULL,
	product_name varchar NOT NULL,
	order_cnt int4 NOT NULL ((order_cnt >= 0))
);