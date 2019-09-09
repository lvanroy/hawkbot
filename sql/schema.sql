BEGIN;

CREATE TABLE Users(
	id VARCHAR PRIMARY KEY,
	username VARCHAR NOT NULL
);

CREATE TABLE Toons(
  id varchar NOT NULL,
  name VARCHAR PRIMARY KEY,
  class VARCHAR NOT NULL
);

CREATE TABLE Gear(
  toon VARCHAR PRIMARY KEY,
  dp INT NOT NULL,
  ap INT NOT NULL,
  aap INT NOT NULL
);

CREATE TABLE Skills(
  id VARCHAR PRIMARY KEY,
  fishing INT NOT NULL,
  trade INT NOT NULL,
  gathering INT NOT NULL,
  training INT NOT NULL,
  farming INT NOT NULL,
  cooking INT NOT NULL,
  alchemy INT NOT NULL,
  sailing INT NOT NULL,
  hunting INT NOT NULL,
  processing INT NOT NULL
);

CREATE TABLE History(
  toon VARCHAR PRIMARY KEY,
  event_date DATE NOT NULL,
  stat VARCHAR NOT NULL,
  amount INT NOT NULL
);

COMMIT;