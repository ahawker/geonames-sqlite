"""
    geonames/sources
    ~~~~~~~~~~~~~~~~

    Contains all sources for geoname gazetteer dump files.
"""
from . import base, records


AlternateName = base.FileSource(
    name='alternate_name',
    record_cls=records.AlternateName,
    fields=[
        'alternate_name_id',
        'geoname_id',
        'iso_language',
        'alternate_name',
        'preferred',
        'short',
        'colloquial',
        'historic',
        'from_period',
        'to_period'
    ]
)


Continent = base.ListSource(
    name='continent',
    record_cls=records.Continent,
    dataset=[
        {'geoname_id': 6255146, 'code': 'AF'},
        {'geoname_id': 6255147, 'code': 'AS'},
        {'geoname_id': 6255148, 'code': 'EU'},
        {'geoname_id': 6255149, 'code': 'NA'},
        {'geoname_id': 6255150, 'code': 'SA'},
        {'geoname_id': 6255151, 'code': 'OC'},
        {'geoname_id': 6255152, 'code': 'AN'}
    ]
)


CountryInfo = base.FileSource(
    name='country_info',
    record_cls=records.CountryInfo,
    fields=[
        'alpha2',
        'alpha3',
        'numeric',
        'fips_code',
        'name',
        'capital',
        'area',
        'population',
        'continent_code',
        'tld',
        'currency_code',
        'currency_name',
        'phone',
        'postal_code_format',
        'postal_code_regex',
        'languages',
        'geoname_id',
        'neighbors',
        'equivalent_fips_code'
    ],
    skip_comments=True
)


FeatureClass = base.ListSource(
    name='feature_class',
    record_cls=records.FeatureClass,
    dataset=[
        {'id': 'A', 'name': 'Administrative boundary features', 'description': 'Country, state, region, etc.'},
        {'id': 'H', 'name': 'Hydrographic features', 'description': 'Stream, lake, etc.'},
        {'id': 'L', 'name': 'Area features', 'description': 'Parks, area, etc.'},
        {'id': 'P', 'name': 'Populated place features', 'description': 'City, village, etc.'},
        {'id': 'R', 'name': 'Road features', 'description': 'Road, railroad, etc.'},
        {'id': 'S', 'name': 'Spot features', 'description': 'Spot, building, farm, etc.'},
        {'id': 'T', 'name': 'Hypsographic features', 'description': 'Mountain, hill, rock, etc.'},
        {'id': 'U', 'name': 'Undersea features', 'description': 'Banks, knoll, etc.'},
        {'id': 'V', 'name': 'Vegetation features', 'description': 'Forest, heath, etc.'}
    ]
)


FeatureCode = base.FileSource(
    name='feature_code',
    record_cls=records.FeatureCode,
    fields=[
        'class_and_code',
        'name',
        'description'
    ]
)

GeonameAllCountries = base.FileSource(
    name='geoname_all_countries',
    record_cls=records.Geoname,
    fields=[
        'geoname_id',
        'name',
        'ascii_name',
        'alternate_names',
        'latitude',
        'longitude',
        'feature_class',
        'feature_code',
        'country_code',
        'country_code2',
        'admin1_code',
        'admin2_code',
        'admin3_code',
        'admin4_code',
        'population',
        'digital_elevation_model',
        'elevation',
        'timezone',
        'last_modified'
    ]
)

GeonameNoCountry = base.FileSource(
    name='geoname_no_country',
    record_cls=records.Geoname,
    fields=[
        'geoname_id',
        'name',
        'ascii_name',
        'alternate_names',
        'latitude',
        'longitude',
        'feature_class',
        'feature_code',
        'country_code',
        'country_code2',
        'fips_code',
        'admin2_code',
        'admin3_code',
        'admin4_code',
        'population',
        'digital_elevation_model',
        'elevation',
        'timezone',
        'last_modified'
    ]
)

Hierarchy = base.FileSource(
    name='hierarchy',
    record_cls=records.Hierarchy,
    fields=[
        'parent_id',
        'child_id',
        'type'
    ]
)


ISOLanguage = base.FileSource(
    name='iso_language',
    record_cls=records.ISOLanguage,
    fields=[
        'code3',
        'code2',
        'code1',
        'name'
    ],
    skip_header=True
)


Shape = base.FileSource(
    name='shape',
    record_cls=records.Shape,
    fields=[
        'geoname_id',
        'geojson'
    ],
    skip_header=True,
    field_size_limit=1000000
)


TimeZone = base.FileSource(
    name='time_zone',
    record_cls=records.TimeZone,
    fields=[
        'country_code_alpha2',
        'name',
        'gmt_offset',
        'dst_offset',
        'raw_offset'
    ],
    skip_header=True
)


UserTag = base.FileSource(
    name='user_tag',
    record_cls=records.UserTag,
    fields=[
        'geoname_id',
        'tag'
    ]
)
