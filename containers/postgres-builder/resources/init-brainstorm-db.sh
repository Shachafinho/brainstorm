#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE users (
		id INTEGER PRIMARY KEY,
		name VARCHAR(80) NOT NULL,
		birthday TIMESTAMPTZ NOT NULL,
		gender CHAR(1) NOT NULL
	);

	CREATE TABLE snapshots (
		user_id INTEGER REFERENCES users(id),
		timestamp TIMESTAMPTZ NOT NULL,

		PRIMARY KEY (user_id, timestamp)
	);

	CREATE TABLE color_images (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,
		width INTEGER NOT NULL,
		height INTEGER NOT NULL,
		data_path VARCHAR(255) NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES snapshots (user_id, timestamp)
	);

	CREATE TABLE depth_images (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,
		width INTEGER NOT NULL,
		height INTEGER NOT NULL,
		data_path VARCHAR(255) NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES snapshots (user_id, timestamp)
	);

	CREATE TABLE feelings (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,
		hunger FLOAT4 NOT NULL,
		thirst FLOAT4 NOT NULL,
		exhaustion FLOAT4 NOT NULL,
		happiness FLOAT4 NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES snapshots (user_id, timestamp)
	);

	CREATE TABLE poses (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES snapshots (user_id, timestamp)
	);

	CREATE TABLE rotations (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,
		x FLOAT8 NOT NULL,
		y FLOAT8 NOT NULL,
		z FLOAT8 NOT NULL,
		w FLOAT8 NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES poses (user_id, snapshot_timestamp)
	);

	CREATE TABLE translations (
		user_id INTEGER NOT NULL,
		snapshot_timestamp TIMESTAMPTZ NOT NULL,
		x FLOAT8 NOT NULL,
		y FLOAT8 NOT NULL,
		z FLOAT8 NOT NULL,

		PRIMARY KEY (user_id, snapshot_timestamp),
		FOREIGN KEY (user_id, snapshot_timestamp) REFERENCES poses (user_id, snapshot_timestamp)
	);


	INSERT INTO users(id, name, birthday, gender)
	VALUES(42, 'Dan Gittik', '1992-03-04 22:00:00+00:00', 'm');
EOSQL
