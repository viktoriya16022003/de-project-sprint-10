DROP TABLE dds.h_category;
CREATE TABLE dds.h_category (
	h_category_pk uuid NOT NULL PRIMARY KEY,
	category_name varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.h_order;
CREATE TABLE dds.h_order (
	h_order_pk uuid NOT NULL PRIMARY KEY ,
	order_id int4 NOT NULL,
	order_dt timestamp NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.h_product;
CREATE TABLE dds.h_product (
	h_product_pk uuid NOT NULL PRIMARY KEY,
	product_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.h_restaurant;
CREATE TABLE dds.h_restaurant (
	h_restaurant_pk uuid NOT NULL PRIMARY KEY,
	restaurant_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.h_user;
CREATE TABLE dds.h_user (
	h_user_pk uuid NOT NULL PRIMARY KEY,
	user_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL
);

DROP TABLE dds.l_order_product;
CREATE TABLE dds.l_order_product (
	hk_order_product_pk uuid NOT NULL PRIMARY KEY,
	h_order_pk uuid NOT NULL,
	h_product_pk uuid NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	FOREIGN KEY (h_order_pk) REFERENCES dds.h_order(h_order_pk),
	FOREIGN KEY (h_product_pk) REFERENCES dds.h_product(h_product_pk)
);

DROP TABLE dds.l_order_user;
CREATE TABLE dds.l_order_user (
	hk_order_user_pk uuid NOT NULL PRIMARY KEY,
	h_order_pk uuid NOT NULL,
	h_user_pk uuid NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	FOREIGN KEY (h_order_pk) REFERENCES dds.h_order(h_order_pk),
	FOREIGN KEY (h_user_pk) REFERENCES dds.h_user(h_user_pk)
);

DROP TABLE dds.l_product_category;
CREATE TABLE dds.l_product_category (
	hk_product_category_pk uuid NOT NULL PRIMARY KEY,
	h_product_pk uuid NOT NULL,
	h_category_pk uuid NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	FOREIGN KEY (h_category_pk) REFERENCES dds.h_category(h_category_pk),
	FOREIGN KEY (h_product_pk) REFERENCES dds.h_product(h_product_pk)
);

DROP TABLE dds.l_product_restaurant;
CREATE TABLE dds.l_product_restaurant (
	hk_product_restaurant_pk uuid NOT NULL PRIMARY KEY ,
	h_product_pk uuid NOT NULL,
	h_restaurant_pk uuid NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	FOREIGN KEY (h_product_pk) REFERENCES dds.h_product(h_product_pk),
	FOREIGN KEY (h_restaurant_pk) REFERENCES dds.h_restaurant(h_restaurant_pk)
);

DROP TABLE dds.s_order_cost;
CREATE TABLE dds.s_order_cost (
	h_order_pk uuid NOT NULL,
	"cost" numeric(19, 5) NOT NULL DEFAULT 0 CHECK ((cost >= (0)::numeric)),
	payment numeric(19, 5) NOT NULL DEFAULT 0  CHECK ((payment >= (0)::numeric)),
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	hk_order_cost_hashdiff uuid NOT NULL UNIQUE,
	PRIMARY KEY (h_order_pk, load_dt),
	FOREIGN KEY (h_order_pk) REFERENCES dds.h_order(h_order_pk)
);

DROP TABLE dds.s_order_status;
CREATE TABLE dds.s_order_status (
	h_order_pk uuid NOT NULL,
	status varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	hk_order_status_hashdiff uuid NOT NULL UNIQUE,
	PRIMARY KEY (h_order_pk, load_dt),
	FOREIGN KEY (h_order_pk) REFERENCES dds.h_order(h_order_pk)
);

DROP TABLE dds.s_product_names;
CREATE TABLE dds.s_product_names (
	h_product_pk uuid NOT NULL,
	"name" varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	hk_product_names_hashdiff uuid NOT NULL UNIQUE,
	PRIMARY KEY (h_product_pk, load_dt),
	FOREIGN KEY (h_product_pk) REFERENCES dds.h_product(h_product_pk)
);

DROP TABLE dds.s_restaurant_names;
CREATE TABLE dds.s_restaurant_names (
	h_restaurant_pk uuid NOT NULL,
	"name" varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	hk_restaurant_names_hashdiff uuid NOT NULL UNIQUE,
	PRIMARY KEY (h_restaurant_pk, load_dt),
	FOREIGN KEY (h_restaurant_pk) REFERENCES dds.h_restaurant(h_restaurant_pk)
);

DROP TABLE dds.s_user_names;
CREATE TABLE dds.s_user_names (
	h_user_pk uuid NOT NULL,
	username varchar NOT NULL,
	userlogin varchar NOT NULL,
	load_dt timestamp NOT NULL,
	load_src varchar NOT NULL,
	hk_user_names_hashdiff uuid NOT NULL UNIQUE,
	PRIMARY KEY (h_user_pk, load_dt),
	FOREIGN KEY (h_user_pk) REFERENCES dds.h_user(h_user_pk)
);