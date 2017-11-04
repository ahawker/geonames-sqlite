-- sql/schema
--
-- Contains table definitions for GeoNames data.
-- Status: WIP

CREATE TABLE IF NOT EXISTS geoname (
  id                    INTEGER PRIMARY KEY     NOT NULL    UNIQUE,
  name                  TEXT                                CHECK (name != ""),
  coordinate_id         INTEGER                 NOT NULL,
  feature_class         TEXT,
  feature_code          TEXT,
  country_code_alpha2   INTEGER,

  population            INTEGER,
  elevation             INTEGER,

  last_modified         TEXT,

  FOREIGN KEY           (coordinate_id)                 REFERENCES  coordinate (id),
  FOREIGN KEY           (feature_class, feature_code)   REFERENCES  feature (class, code),
  FOREIGN KEY           (country_code_alpha2)           REFERENCES  country (country_code_alpha2)
);

CREATE TABLE IF NOT EXISTS alternate_name (
  id            INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  geoname_id    INTEGER             NOT NULL,
  type          TEXT,
  name          TEXT                NOT NULL    CHECK (name != ""),
  preferred     INTEGER             DEFAULT 0,
  short         INTEGER             DEFAULT 0,
  colloquial    INTEGER             DEFAULT 0,
  historic      INTEGER             DEFAULT 0,

  FOREIGN KEY   (geoname_id)        REFERENCES  geoname (id)
);

CREATE TABLE IF NOT EXISTS coordinate (
  id        INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  latitude  REAL                            CHECK (latitude >= -90 AND latitude <= 90),
  longitude REAL                            CHECK (longitude >= -180 AND longitude <= 180)
);

CREATE TABLE IF NOT EXISTS approximate_coordinate (
  id            INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  coordinate_id INTEGER             NOT NULL,
  radius        INTEGER             NOT NULL,

  FOREIGN KEY   (coordinate_id)     REFERENCES  coordinate (id)
);

CREATE TABLE IF NOT EXISTS feature (
  class         TEXT                NOT NULL    CHECK (class != ""),
  code          TEXT                NOT NULL    CHECK (code != ""),
  description   TEXT,

  PRIMARY KEY   (class, code)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS fips_code (
  code  TEXT    PRIMARY KEY NOT NULL    UNIQUE  CHECK (code != "")
  -- TODO
);

CREATE TABLE IF NOT EXISTS admin (
  id            INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  geoname_id    INTEGER             NOT NULL,
  code          TEXT                NOT NULL    CHECK (code != ""),
  level         INTEGER             NOT NULL    CHECK (level >= 0 AND level <= 4),

  FOREIGN KEY   (geoname_id)        REFERENCES  geoname (id)
);

CREATE TABLE IF NOT EXISTS currency (
  code  TEXT    PRIMARY KEY NOT NULL    UNIQUE  CHECK (code != ""),
  name  TEXT                NOT NULL            CHECK (name != "")
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS postal_code (
  id        INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  format    TEXT,
  regex     TEXT
);

CREATE TABLE IF NOT EXISTS language (
  code                  TEXT    PRIMARY KEY     NOT NULL    UNIQUE  CHECK (code != ""),
  country_code_alpha2   TEXT,

  FOREIGN KEY           (country_code_alpha2)   REFERENCES  country_code  (alpha2)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS country_code (
  alpha2    TEXT    PRIMARY KEY NOT NULL    UNIQUE  CHECK (alpha2 != ""),
  alpha3    TEXT                NOT NULL    UNIQUE  CHECK (alpha3 != ""),
  numeric   TEXT                NOT NULL    UNIQUE  CHECK (numeric != "")
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS country (
  geoname_id            INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  country_code_alpha2   TEXT                NOT NULL,
  country_code_alpha3   TEXT                NOT NULL,
  country_code_numeric  TEXT                NOT NULL,
  name                  TEXT,
  capital               TEXT,
  area                  INTEGER                         CHECK (area > 0),
  population            INTEGER                         CHECK (population > 0),
  continent_geoname_id  INTEGER             NOT NULL    CHECK (continent_geoname_id > 0),
  tld                   TEXT,
  currency_code         TEXT
  phone                 TEXT,
  postal_code_id        INTEGER,

  FOREIGN KEY   (country_code_alpha2)          REFERENCES  country_code (alpha2),
  FOREIGN KEY   (country_code_alpha3)          REFERENCES  country_code (alpha3),
  FOREIGN KEY   (country_code_numeric)         REFERENCES  country_code (numeric),
  FOREIGN KEY   (continent_geoname_id)      REFERENCES  continent (geoname_id),
  FOREIGN KEY   (currency_code)             REFERENCES  currency (code),
  FOREIGN KEY   (postal_code_id)             REFERENCES  postal_code (id)
);

CREATE TABLE IF NOT EXISTS country_neighbors (
  country_geoname_id    INTEGER NOT NULL,
  neighbor_geoname_id   INTEGER NOT NULL,

  FOREIGN KEY           (country_geoname_id)    REFERENCES  country (geoname_id),
  FOREIGN KEY           (neighbor_geoname_id)   REFERENCES  country (geoname_id)
);

CREATE TABLE IF NOT EXISTS continent (
  geoname_id    INTEGER PRIMARY KEY NOT NULL    UNIQUE,
  code          TEXT                                    CHECK (code != ""),
  name          TEXT                NOT NULL            CHECK (name != "")
);

CREATE TABLE IF NOT EXISTS timezone (
  name                  TEXT    PRIMARY KEY NOT NULL    UNIQUE  CHECK (name != ""),
  country_code_alpha2   TEXT,
  gmt_offset            REAL,
  dst_offset            REAL,
  raw_offset            REAL,

  FOREIGN KEY           (country_code_alpha2)           REFERENCES  country_code (alpha2)
);
