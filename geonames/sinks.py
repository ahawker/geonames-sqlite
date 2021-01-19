"""
    geonames/sinks
    ~~~~~~~~~~~~~~

    Contains sinks for all sqlite tables.
"""
from . import base, exceptions, records, tables


Abbreviation = base.RecordSink[records.AlternateName](
    name='abbreviation',
    table=tables.Abbreviation,
    predicate=lambda r: r.is_abbreviation,
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'name': r.alternate_name
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


AdminCode = base.FlattenRecordFieldSink[records.Geoname](
    name='admin_code',
    table=tables.AdminCode,
    field_name='admin_codes',
    field_predicate=lambda r, f: bool(f),
    transform=lambda r, f, i: {
        'geoname_id': r.geoname_id,
        'code': f,
        'level': i + 1
    }
)


AirportCode = base.RecordSink[records.AlternateName](
    name='airport_code',
    table=tables.AirportCode,
    predicate=lambda r: r.is_airport_code,
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'type': r.iso_language,
        'code': r.alternate_name
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


AlternateCountryCode = base.FlattenRecordFieldSink[records.Geoname](
    name='alternate_country_code',
    table=tables.AlternateCountryCode,
    field_name='alternate_country_codes_set',
    transform=lambda r, f, _i: {
        'geoname_id': r.geoname_id,
        'country_code_alpha2': f if f != 'UK' else 'GB'
    }
)


AlternateName = base.RecordSink[records.AlternateName](
    name='alternate_name',
    table=tables.AlternateName,
    predicate=lambda r: not r.iso_language or r.iso_language.lower() == 'en',
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'language_code': r.iso_language,
        'name': r.alternate_name,
        'preferred': r.preferred,
        'short': r.short,
        'colloquial': r.colloquial,
        'historic': r.historic,
        'from_period': r.from_period,
        'to_period': r.to_period
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


Boundary = base.RecordSink[records.Shape](
    name='boundary',
    table=tables.Boundary,
    transform=lambda r: {
        'id': r.geoname_id,
        'geojson': r.geojson
    }
)


Continent = base.RecordSink[records.Continent](
    name='continent',
    table=tables.Continent,
    transform=lambda r: {
        'id': r.geoname_id,
        'code': r.code
    }
)


Country = base.RecordSink[records.CountryInfo](
    name='country',
    table=tables.Country,
    transform=lambda r: {
        'id': r.geoname_id,
        'country_code_alpha2': r.alpha2,
        'name': r.name,
        'capital': r.capital,
        'area': r.area,
        'population': r.population,
        'continent_code': r.continent_code,
        'currency_code': r.currency_code,
        'tld': r.tld,
        'phone': r.phone,
        'postal_code_format': r.postal_code_format,
        'postal_code_regex': r.postal_code_regex
    }
)


CountryCode = base.RecordSink[records.CountryInfo](
    name='country_code',
    table=tables.CountryCode,
    transform=lambda r: {
        'alpha2': r.alpha2,
        'alpha3': r.alpha3,
        'numeric': r.numeric
    }
)


CountryLanguage = base.FlattenRecordFieldSink[records.CountryInfo](
    name='country_language',
    table=tables.CountryLanguage,
    field_name='languages_with_country_code',
    predicate=lambda r: bool(r.languages),
    transform=lambda r, f, _i: {
        'country_id': r.geoname_id,
        'language_code': f[0],
        'country_code_alpha2': f[1]
    }
)


CountryNeighbor = base.FlattenRecordFieldSink[records.CountryInfo](
    name='country_neighbor',
    table=tables.CountryNeighbor,
    field_name='neighbors',
    predicate=lambda r: bool(r.neighbors),
    transform=lambda r, f, _i: {
        'country_id': r.geoname_id,
        'neighbor_country_code_alpha2': f
    }
)


Currency = base.RecordSink[records.CountryInfo](
    name='currency',
    table=tables.Currency,
    transform=lambda r: {
        'code': r.currency_code,
        'name': r.currency_name
    }
)


FeatureClass = base.RecordSink[records.FeatureClass](
    name='feature_class',
    table=tables.FeatureClass,
    transform=lambda r: {
        'id': r.id,
        'name': r.name,
        'description': r.description
    }
)


FeatureCode = base.RecordSink[records.FeatureCode](
    name='feature_code',
    table=tables.FeatureCode,
    predicate=lambda r: r.class_and_code != 'null',
    transform=lambda r: {
        'id': r.class_and_code.split('.')[1],
        'class': r.class_and_code.split('.')[0],
        'name': r.name,
        'description': r.description
    }
)


Geoname = base.RecordSink[records.Geoname](
    name='geoname',
    table=tables.Geoname,
    transform=lambda r: {
        'id': r.geoname_id,
        'name': r.name,
        'latitude': r.latitude,
        'longitude': r.longitude,
        'feature_class': r.feature_class,
        'feature_code': r.feature_code,
        'country_code': r.country_code,
        'population': r.population,
        'elevation': r.elevation,
        'last_modified': r.last_modified
    },
    exception_handler=exceptions.ignore_unique_key_constraint
)


Hierarchy = base.RecordSink[records.Hierarchy](
    name='hierarchy',
    table=tables.Hierarchy,
    predicate=lambda r: r.type and r.type == 'ADM',
    transform=lambda r: {
        'id': r.child_id,
        'parent_id': r.parent_id
    }
)


LanguageCode = base.RecordSink[records.ISOLanguage](
    name='language_code',
    table=tables.LanguageCode,
    transform=lambda r: {
        'code3': r.code3 or r.code2,
        'code2': r.code2 or r.code3,
        'code1': r.code1,
        'name': r.name
    },
    exception_handler=exceptions.ignore_unique_key_constraint
)


Location = base.RecordSink[records.Geoname](
    name='location',
    table=tables.Location,
    transform=lambda r: {
        'id': r.geoname_id,
        'latitude': r.latitude,
        'longitude': r.longitude,
    },
    exception_handler=exceptions.ignore_unique_key_constraint
)


PostalCode = base.RecordSink[records.AlternateName](
    name='postal_code',
    table=tables.PostalCode,
    predicate=lambda r: r.is_postal_code,
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'code': r.alternate_name
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


PostalCodeSpec = base.RecordSink[records.CountryInfo](
    name='postal_code_spec',
    table=tables.PostalCodeSpec,
    transform=lambda r: {
        'format': r.postal_code_format,
        'regex': r.postal_code_regex
    }
)


TimeZone = base.RecordSink[records.TimeZone](
    name='time_zone',
    table=tables.TimeZone,
    transform=lambda r: {
        'name': r.name,
        'country_code_alpha2': r.country_code_alpha2,
        'gmt_offset': r.gmt_offset,
        'dst_offset': r.dst_offset,
        'raw_offset': r.raw_offset
    }
)


UserLink = base.RecordSink[records.AlternateName](
    name='user_link',
    table=tables.UserLink,
    predicate=lambda r: r.is_link,
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'link': r.alternate_name
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


UserTag = base.RecordSink[records.UserTag](
    name='user_tag',
    table=tables.UserTag,
    transform=lambda r: {
        'geoname_id': r.geoname_id,
        'tag': r.tag
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)


Wikidata = base.RecordSink[records.AlternateName](
    name='wikidata',
    table=tables.Wikidata,
    predicate=lambda r: r.is_wikidata_id,
    transform=lambda r: {
        'id': r.alternate_name_id,
        'geoname_id': r.geoname_id,
        'wikidata_id': r.alternate_name
    },
    exception_handler=exceptions.ignore_foreign_key_constraint
)
