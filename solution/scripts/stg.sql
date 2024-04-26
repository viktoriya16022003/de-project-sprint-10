-- DROP TABLE stg.order_events;

CREATE TABLE stg.order_events(
	id serial4 NOT NULL PRIMARY KEY,
	object_id int4 NOT NULL UNIQUE,
	payload json NOT NULL,
	object_type varchar NOT NULL,
	sent_dttm timestamp NOT NULL
);