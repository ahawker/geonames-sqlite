"""
    geonames/records
    ~~~~~~~~~~~~~~~~

    Contains record types for all data sources.
"""
from typing import Any, Optional, List, Set

from pydantic import confloat, constr, validator

from . import base, validators


AIRPORT_CODES = ('iata', 'icao', 'faac', 'tcid', 'unlc')


class AlternateName(base.Record):
    """
    Represents a record from an individual line of an alternate names data source.
    """
    row_num: int
    alternate_name_id: int
    geoname_id: int
    iso_language: Optional[str]
    alternate_name: str
    preferred: Optional[bool]
    short: Optional[bool]
    colloquial: Optional[bool]
    historic: Optional[bool]
    from_period: Optional[str]
    to_period: Optional[str]

    @property
    def is_airport_code(self):
        return self.iso_language in AIRPORT_CODES

    @property
    def is_alternate_name(self):
        return len(self.iso_language) <= 3

    @property
    def is_abbreviation(self):
        return self.iso_language == 'abbr'

    @property
    def is_wikidata_id(self):
        return self.iso_language == 'wkdt'

    @property
    def is_link(self):
        return self.iso_language == 'link'

    @property
    def is_postal_code(self):
        return self.iso_language == 'post'

    @validator('preferred', 'short', 'colloquial', 'historic', pre=True)
    def optional_int_to_bool(cls, value) -> Any:
        return validators.optional_int_to_bool(value)


class Continent(base.Record):
    """
    Record that represents a continent.
    """
    row_num: int
    geoname_id: int
    code: str


class CountryInfo(base.Record):
    row_num: int
    alpha2: constr(min_length=2, max_length=2)
    alpha3: constr(min_length=3, max_length=3)
    numeric: int
    fips_code: Optional[str]
    name: str
    capital: Optional[str]
    area: float
    population: int
    continent_code: str
    tld: Optional[constr(regex=r'\.\w+')]
    currency_code: Optional[str]
    currency_name: Optional[str]
    phone: Optional[str]
    postal_code_format: Optional[str]
    postal_code_regex: Optional[str]
    languages: Optional[Set[str]]
    geoname_id: int
    neighbors: Optional[Set[str]]
    equivalent_fips_code: Optional[str]

    @property
    def languages_with_country_code(self):
        result = []
        for language in self.languages:
            if '-' in language:
                lcode, ccode = language.split('-')
            else:
                lcode, ccode = language, None
            result.append((lcode, ccode))
        return result

    @validator('numeric')
    def numeric_zero_to_none(cls, value: int) -> Optional[int]:
        return validators.zero_to_none(value)

    @validator('languages', 'neighbors', pre=True)
    def csv_str_to_list(cls, value: str) -> List[str]:
        return validators.csv_str_to_list(value)


class FeatureClass(base.Record):
    row_num: int
    id: str
    name: str
    description: str


class FeatureCode(base.Record):
    row_num: int
    class_and_code: str
    name: str
    description: Optional[str]


class Geoname(base.Record):
    row_num: int
    geoname_id: int
    name: str
    ascii_name: Optional[str]
    alternate_names: Optional[Set[str]]
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
    feature_class: Optional[str]
    feature_code: Optional[str]
    country_code: Optional[str]
    country_code2: Optional[Set[str]]
    admin1_code: Optional[str]
    admin2_code: Optional[str]
    admin3_code: Optional[str]
    admin4_code: Optional[str]
    population: int
    digital_elevation_model: Optional[str]
    elevation: Optional[int]
    timezone: Optional[str]
    last_modified: str

    @property
    def admin_codes(self):
        return [
            self.admin1_code,
            self.admin2_code,
            self.admin3_code,
            self.admin4_code
        ]

    @property
    def alternate_country_codes_set(self):
        if not self.country_code2:
            return set()
        return self.country_code2.difference({self.country_code})

    @property
    def alternate_names_set(self):
        if not self.alternate_names:
            return set()
        return self.alternate_names.difference({self.name, self.ascii_name})

    @validator('alternate_names', 'country_code2', pre=True)
    def csv_str_to_list(cls, value: str) -> List[str]:
        return validators.csv_str_to_list(value)

    @validator('elevation', pre=True)
    def elevation_neg_9999_to_none(cls, value: str) -> Optional[int]:
        return validators.sentinel_to_none(value, '-9999')


class Hierarchy(base.Record):
    row_num: int
    parent_id: int
    child_id: int
    type: Optional[str]


class ISOLanguage(base.Record):
    row_num: int
    code3: Optional[str]
    code2: Optional[str]
    code1: Optional[str]
    name: str

    @validator('code2', pre=True)
    def slash_to_old_code2(cls, value: str) -> str:
        return value.split('/')[-1].strip(' *') if '/' in value else value


class Shape(base.Record):
    row_num: int
    geoname_id: int
    geojson: str


class TimeZone(base.Record):
    row_num: int
    country_code_alpha2: constr(min_length=2, max_length=2)
    name: str
    dst_offset: confloat(ge=-12, le=14)
    raw_offset: confloat(ge=-12, le=14)
    gmt_offset: confloat(ge=-12, le=14)


class UserTag(base.Record):
    row_num: int
    geoname_id: int
    tag: str
