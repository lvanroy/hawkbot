BEGIN;

CREATE TABLE Users(
	id varchar PRIMARY KEY,
	username VARCHAR
);

CREATE TABLE Toons(
  id varchar,
  name VARCHAR,
  class VARCHAR,
  PRIMARY KEY (id, name)
);

CREATE TABLE Gear(
  id varchar PRIMARY KEY,
  dp INT,
  ap INT,
  aap INT
);

CREATE TABLE Skills(
  id varchar PRIMARY KEY,
  fishing INT,
  trading INT,
  gathering INT,
  training INT,
  farming INT,
  cooking INT,
  alchemy INT,
  sailing INT,
  hunting INT
);

COMMIT;