"""
    geonames/tables
    ~~~~~~~~~~~~~~~

    Contains sqlite table definitions.
"""
from . import base


Abbreviation = base.Table(
    name='abbreviation',
    table="""
CREATE TABLE IF NOT EXISTS abbreviation (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    name          TEXT                NOT NULL    CHECK (name != ""),

    FOREIGN KEY   (geoname_id)                    REFERENCES geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS abbreviation_geoname_id_idx ON abbreviation (geoname_id);
""",
    modify="""
INSERT INTO abbreviation (
    id,
    geoname_id,
    name
) VALUES (
    :id,
    :geoname_id,
    :name
);
""")


AdminCode = base.Table(
    name='admin_code',
    table="""
CREATE TABLE IF NOT EXISTS admin_code (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    code          TEXT                NOT NULL      CHECK (code != ""),
    level         INTEGER             NOT NULL      CHECK (level >= 1 AND level <= 4),

    FOREIGN KEY   (geoname_id)                      REFERENCES  geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS admin_code_geoname_id_idx    ON admin_code (geoname_id);
CREATE INDEX IF NOT EXISTS admin_code_level_idx         ON admin_code (level);
""",
    modify="""
INSERT INTO admin_code (
    geoname_id,
    code,
    level
) VALUES (
    :geoname_id,
    :code,
    :level
);
""")


AirportCode = base.Table(
    name='airport_code',
    table="""
CREATE TABLE IF NOT EXISTS airport_code (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    type          TEXT                NOT NULL,
    code          TEXT                NOT NULL    CHECK (code != ""),

    FOREIGN KEY   (geoname_id)                    REFERENCES geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS airport_code_geoname_id_idx ON airport_code (geoname_id);
""",
    modify="""
INSERT INTO airport_code (
    id,
    geoname_id,
    type,
    code
) VALUES (
    :id,
    :geoname_id,
    :type,
    :code
);
""")


AlternateCountryCode = base.Table(
    name='alternate_country_code',
    table="""
CREATE TABLE IF NOT EXISTS alternate_country_code (
    id                    INTEGER PRIMARY KEY     NOT NULL,
    geoname_id            INTEGER                 NOT NULL,
    country_code_id       INTEGER                 NOT NULL,

    FOREIGN KEY           (geoname_id)            REFERENCES  geoname (id),
    FOREIGN KEY           (country_code_id)       REFERENCES  country_code (id)
);
""",
    indices="""
CREATE UNIQUE INDEX IF NOT EXISTS alternate_country_code_geoname_country_code_uniq_idx  ON alternate_country_code(geoname_id, country_code_id);
CREATE INDEX IF NOT EXISTS alternate_country_code_geoname_id_idx                        ON alternate_country_code (geoname_id);
CREATE INDEX IF NOT EXISTS alternate_country_code_country_code_id_idx                   ON alternate_country_code (country_code_id);
""",
    modify="""
INSERT INTO alternate_country_code (
    geoname_id,
    country_code_id
) VALUES (
    :geoname_id,
    (SELECT id FROM country_code WHERE alpha2=:country_code_alpha2)
);
""")


AlternateName = base.Table(
    name='alternate_name',
    table="""
CREATE TABLE IF NOT EXISTS alternate_name (
    id                INTEGER PRIMARY KEY NOT NULL,
    geoname_id        INTEGER             NOT NULL,
    language_code_id  INTEGER,
    name              TEXT                NOT NULL    CHECK (name != ""),
    preferred         INTEGER             DEFAULT 0,
    short             INTEGER             DEFAULT 0,
    colloquial        INTEGER             DEFAULT 0,
    historic          INTEGER             DEFAULT 0,
    from_period       TEXT                            CHECK (from_period != ""),
    to_period         TEXT                            CHECK (to_period != ""),

    FOREIGN KEY   (geoname_id)                        REFERENCES geoname (id),
    FOREIGN KEY   (language_code_id)                  REFERENCES language_code (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS alternate_name_geoname_id_idx        ON alternate_name (geoname_id);
CREATE INDEX IF NOT EXISTS alternate_name_language_code_id_idx  ON alternate_name (language_code_id);
""",
    modify="""
INSERT INTO alternate_name (
    id,
    geoname_id,
    language_code_id,
    name,
    preferred,
    short,
    colloquial,
    historic,
    from_period,
    to_period
) VALUES (
    :id,
    :geoname_id,
    (SELECT id FROM language_code WHERE code3=:language_code OR code2=:language_code OR code1=:language_code),
    :name,
    :preferred,
    :short,
    :colloquial,
    :historic,
    :from_period,
    :to_period
);
""")


Boundary = base.Table(
    name='boundary',
    table="""
CREATE TABLE IF NOT EXISTS boundary (
    id            INTEGER PRIMARY KEY NOT NULL,
    geojson       TEXT                NOT NULL    CHECK (geojson != "")
);
""",
    indices=None,
    modify="""
INSERT INTO boundary (
    id,
    geojson
) VALUES (
    :id,
    :geojson
);
""")


Continent = base.Table(
    name='continent',
    table="""
CREATE TABLE IF NOT EXISTS continent (
    id    INTEGER PRIMARY KEY,
    code  TEXT                NOT NULL    UNIQUE
);
""",
    indices=None,
    modify="""
INSERT INTO continent (
    id,
    code
) VALUES (
    :id,
    :code
);
""")


Country = base.Table(
    name='country',
    table="""
CREATE TABLE IF NOT EXISTS country (
    id                    INTEGER PRIMARY KEY NOT NULL,
    country_code_id       INTEGER             NOT NULL,
    name                  TEXT,
    capital               TEXT,
    area                  INTEGER                         CHECK (area >= 0),
    population            INTEGER                         CHECK (population >= 0),
    continent_id          INTEGER,
    tld                   TEXT,
    currency_code         TEXT,
    phone                 TEXT,
    postal_code_format    TEXT,
    postal_code_regex     TEXT,

    FOREIGN KEY           (country_code_id)               REFERENCES country_code (id),
    FOREIGN KEY           (continent_id)                  REFERENCES continent (id),
    FOREIGN KEY           (currency_code)                 REFERENCES currency (code)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS country_country_code_id_idx      ON country (country_code_id);
CREATE INDEX IF NOT EXISTS country_continent_id_idx         ON country (continent_id);
""",
    modify="""
INSERT INTO country (
    id,
    country_code_id,
    name,
    capital,
    area,
    population,
    continent_id,
    tld,
    currency_code,
    phone,
    postal_code_format,
    postal_code_regex
) VALUES (
    :id,
    (SELECT id FROM country_code WHERE alpha2=:country_code_alpha2),
    :name,
    :capital,
    :area,
    :population,
    (SELECT id FROM continent WHERE code=:continent_code),
    :tld,
    :currency_code,
    :phone,
    :postal_code_format,
    :postal_code_regex
);
""")

#(SELECT id FROM postal_code_spec WHERE format=:postal_code_format AND regex=:postal_code_regex)


CountryCode = base.Table(
    name='country_code',
    table="""
CREATE TABLE IF NOT EXISTS country_code (
    id        INTEGER PRIMARY KEY NOT NULL,
    alpha2    TEXT                NOT NULL    UNIQUE  CHECK (alpha2 != ""),
    alpha3    TEXT                NOT NULL    UNIQUE  CHECK (alpha3 != ""),
    numeric   INTEGER                         UNIQUE  CHECK (numeric >= 0)
);
""",
    indices=None,
    modify="""
INSERT INTO country_code (
    alpha2,
    alpha3,
    numeric
) VALUES (
    :alpha2,
    :alpha3,
    :numeric
);
""")


CountryLanguage = base.Table(
    name='country_language',
    table="""
CREATE TABLE IF NOT EXISTS country_language (
    id                    INTEGER PRIMARY KEY NOT NULL,
    country_id            INTEGER             NOT NULL,
    language_code_id      INTEGER             NOT NULL,
    country_code_id       INTEGER,

    FOREIGN KEY           (language_code_id)                          REFERENCES language_code (id),
    FOREIGN KEY           (country_code_id)                           REFERENCES country_code (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS country_language_language_code_id_idx    ON country_language (language_code_id);
CREATE INDEX IF NOT EXISTS country_language_country_code_id_idx     ON country_language (country_code_id);
""",
    modify="""
INSERT INTO country_language (
    country_id,
    language_code_id,
    country_code_id
) VALUES (
    :country_id,
    (SELECT id FROM language_code WHERE code3=:language_code OR code2=:language_code OR code1=:language_code),
    (SELECT id FROM country_code WHERE alpha2=:country_code_alpha2)
);
""")


CountryNeighbor = base.Table(
    name='country_neighbor',
    table="""
CREATE TABLE IF NOT EXISTS country_neighbor (
    id                    INTEGER PRIMARY KEY NOT NULL,
    country_id            INTEGER             NOT NULL,
    neighbor_id           INTEGER             NOT NULL,             

    FOREIGN KEY           (country_id)        REFERENCES geoname (id),
    FOREIGN KEY           (neighbor_id)       REFERENCES geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS country_neighbor_country_id_idx  ON country_neighbor (country_id);
CREATE INDEX IF NOT EXISTS country_neighbor_neighbor_id_idx ON country_neighbor (neighbor_id);
    """,
    modify="""
INSERT INTO country_neighbor (
    country_id,
    neighbor_id
) VALUES (
    :country_id,
    (SELECT country.id
     FROM country
     INNER JOIN country_code ON country.country_code_id = country_code.id
     WHERE country_code.alpha2=:neighbor_country_code_alpha2)
);
""")


Currency = base.Table(
    name='currency',
    table="""
CREATE TABLE IF NOT EXISTS currency (
    code  TEXT    PRIMARY KEY NOT NULL            CHECK (code != ""),
    name  TEXT                NOT NULL            CHECK (name != "")
) WITHOUT ROWID;
""",
    indices=None,
    modify="""
INSERT OR IGNORE INTO currency (
    code,
    name
) VALUES (
    :code,
    :name
);
""")


FeatureClass = base.Table(
    name='feature_class',
    table="""
CREATE TABLE IF NOT EXISTS feature_class (
    id            TEXT    PRIMARY KEY NOT NULL    CHECK (id != ""),
    name          TEXT                NOT NULL    CHECK (name != ""),
    description   TEXT
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS feature_class_name_idx ON feature_class (name);
""",
    modify="""
INSERT INTO feature_class (
    id,
    name,
    description
) VALUES (
    :id,
    :name,
    :description
);
""")


FeatureCode = base.Table(
    name='feature_code',
    table="""
CREATE TABLE IF NOT EXISTS feature_code (
    id                TEXT    PRIMARY KEY NOT NULL    CHECK (id != ""),
    class             TEXT                NOT NULL    CHECK (class != ""),
    name              TEXT                NOT NULL    CHECK (name != ""),
    description       TEXT,

    FOREIGN KEY       (class)             REFERENCES  feature_class (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS feature_code_class_idx ON feature_code (class);
""",
    modify="""
INSERT INTO feature_code (
    id,
    class,
    name,
    description
) VALUES (
    :id,
    :class,
    :name,
    :description
);
""")


Geoname = base.Table(
    name='geoname',
    table="""
CREATE TABLE IF NOT EXISTS geoname (
    id                    INTEGER PRIMARY KEY     NOT NULL,
    name                  TEXT                                CHECK (name != ""),
    parent_id             INTEGER,
    location_id           INTEGER                 NOT NULL,
    feature_class_id      TEXT,
    feature_code_id       TEXT,
    country_code_id       INTEGER,

    population            INTEGER,
    elevation             INTEGER,

    last_modified         TEXT                                CHECK (last_modified != ""),

    FOREIGN KEY           (parent_id)                         REFERENCES geoname (id),
    FOREIGN KEY           (location_id)                       REFERENCES location (id),
    FOREIGN KEY           (feature_class_id)                  REFERENCES feature_class (id),
    FOREIGN KEY           (feature_code_id)                   REFERENCES feature_code (id),
    FOREIGN KEY           (country_code_id)                   REFERENCES country_code (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS geoname_parent_id_idx            ON geoname (parent_id);
CREATE INDEX IF NOT EXISTS geoname_location_id_idx          ON geoname (location_id);
CREATE INDEX IF NOT EXISTS geoname_feature_class_id_idx     ON geoname (feature_class_id);
CREATE INDEX IF NOT EXISTS geoname_feature_code_id_idx      ON geoname (feature_code_id);
CREATE INDEX IF NOT EXISTS geoname_country_code_id_idx      ON geoname (country_code_id);
CREATE INDEX IF NOT EXISTS geoname_last_modified_idx        ON geoname (last_modified);
""",
    modify="""
INSERT INTO geoname (
    id,
    name,
    parent_id,
    location_id,
    feature_class_id,
    feature_code_id,
    country_code_id,
    population,
    elevation,
    last_modified
) VALUES (
    :id,
    :name,
    NULL,
    (SELECT id FROM location WHERE latitude=:latitude AND longitude=:longitude),
    (SELECT id FROM feature_class WHERE id=:feature_class),
    (SELECT id FROM feature_code WHERE id=:feature_code),
    (SELECT id FROM country_code WHERE alpha2=:country_code),
    :population,
    :elevation,
    :last_modified
);
""")


Hierarchy = base.Table(
    name='hierarchy',
    table=None,
    indices=None,
    modify="""
UPDATE geoname
SET
    parent_id=:parent_id
WHERE
    id=:id;
""")


LanguageCode = base.Table(
    name='language_code',
    table="""
CREATE TABLE IF NOT EXISTS language_code (
    id    INTEGER PRIMARY KEY     NOT NULL,
    code3 TEXT                    NOT NULL    UNIQUE      CHECK (code3 != ""),
    code2 TEXT                                UNIQUE      CHECK (code2 != ""),
    code1 TEXT                                UNIQUE      CHECK (code1 != ""),
    name  TEXT                    NOT NULL    UNIQUE      CHECK (name != "")
);
""",
    indices=None,
    modify="""
INSERT INTO language_code (
    code3,
    code2,
    code1,
    name
) VALUES (
    :code3,
    :code2,
    :code1,
    :name
);
""")


Location = base.Table(
    name='location',
    table="""
CREATE TABLE IF NOT EXISTS location (
    id        INTEGER PRIMARY KEY     NOT NULL,
    latitude  REAL                                        CHECK (latitude >= -90 AND latitude <= 90),
    longitude REAL                                        CHECK (longitude >= -180 AND longitude <= 180)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS location_latitude_longitude_idx ON location(latitude, longitude);
""",
    modify="""
INSERT INTO location (
    id,
    latitude,
    longitude
) VALUES (
    :id,
    :latitude,
    :longitude
);
""")


PostalCode = base.Table(
    name='postal_code',
    table="""
CREATE TABLE IF NOT EXISTS postal_code (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    code          TEXT                NOT NULL    CHECK (code != ""),

    FOREIGN KEY   (geoname_id)                    REFERENCES geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS postal_code_geoname_id_idx ON postal_code (geoname_id);
""",
    modify="""
INSERT INTO postal_code (
    id,
    geoname_id,
    code
) VALUES (
    :id,
    :geoname_id,
    :code
);
""")


PostalCodeSpec = base.Table(
    name='postal_code_spec',
    table="""
CREATE TABLE IF NOT EXISTS postal_code_spec (
    id        INTEGER PRIMARY KEY NOT NULL,
    format    TEXT,
    regex     TEXT
);
""",
    indices="""
CREATE UNIQUE INDEX IF NOT EXISTS postal_code_spec_format_regex_uniq_idx ON postal_code(format, regex);
""",
    modify="""
INSERT OR IGNORE INTO postal_code_spec (
    format,
    regex
) VALUES (
    :format,
    :regex
);
""")


TimeZone = base.Table(
    name='time_zone',
    table="""
CREATE TABLE IF NOT EXISTS time_zone (
    name                  TEXT    PRIMARY KEY NOT NULL    CHECK (name != ""),
    country_code_id       INTEGER             NOT NULL,
    gmt_offset            REAL                            CHECK (gmt_offset >= -12 AND gmt_offset <= 14),
    dst_offset            REAL                            CHECK (dst_offset >= -12 AND dst_offset <= 14),
    raw_offset            REAL                            CHECK (raw_offset >= -12 AND raw_offset <= 14),

    FOREIGN KEY           (country_code_id)               REFERENCES  country_code (id)
) WITHOUT ROWID;
""",
    indices=None,
    modify="""
INSERT INTO time_zone (
    name,
    country_code_id,
    gmt_offset,
    dst_offset,
    raw_offset
) VALUES (
    :name,
    (SELECT id FROM country_code where alpha2=:country_code_alpha2),
    :gmt_offset,
    :dst_offset,
    :raw_offset
);
""")


UserLink = base.Table(
    name='user_link',
    table="""
CREATE TABLE IF NOT EXISTS user_link (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    link          TEXT                NOT NULL            CHECK (link != ""),

    FOREIGN KEY   (geoname_id)                            REFERENCES  geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS user_link_geoname_id_idx ON user_link (geoname_id);
""",
    modify="""
INSERT INTO user_link (
    id,
    geoname_id,
    link
) VALUES (
    :id,
    :geoname_id,
    :link
);
""")


UserTag = base.Table(
    name='user_tag',
    table="""
CREATE TABLE IF NOT EXISTS user_tag (
    id            INTEGER PRIMARY KEY NOT NULL,
    geoname_id    INTEGER             NOT NULL,
    tag           TEXT                NOT NULL            CHECK (tag != ""),

    FOREIGN KEY   (geoname_id)                            REFERENCES  geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS user_tag_geoname_id_idx ON user_tag (geoname_id);
""",
    modify="""
INSERT INTO user_tag (
    geoname_id,
    tag
) VALUES (
    :geoname_id,
    :tag
);
""")


Wikidata = base.Table(
    name='wikidata',
    table="""
CREATE TABLE IF NOT EXISTS wikidata (
  id            INTEGER PRIMARY KEY NOT NULL,
  geoname_id    INTEGER             NOT NULL,
  wikidata_id   TEXT                NOT NULL    CHECK (wikidata_id != ""),

  FOREIGN KEY   (geoname_id)                    REFERENCES geoname (id)
);
""",
    indices="""
CREATE INDEX IF NOT EXISTS wikidata_name_geoname_id_idx ON wikidata (geoname_id);
""",
    modify="""
INSERT INTO wikidata (
    id,
    geoname_id,
    wikidata_id
) VALUES (
    :id,
    :geoname_id,
    :wikidata_id
);
""")


