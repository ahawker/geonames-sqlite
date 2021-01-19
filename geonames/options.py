"""
    geonames/options
    ~~~~~~~~~~~~~~~~

    Contains configuration functionality.
"""
import dataclasses

from typing import Dict, Optional


@dataclasses.dataclass
class Source:
    path: Optional[str] = None
    enabled: bool = True


@dataclasses.dataclass
class Sink:
    enabled: bool = True


@dataclasses.dataclass
class Pipeline:
    sinks: Dict[str, Sink]
    sources: Dict[str, Source]


Graph = Pipeline(
    sinks=dict(
        abbreviation=Sink(),
        admin_code=Sink(),
        airport_code=Sink(),
        alternate_country_code=Sink(),
        alternate_name=Sink(),
        boundary=Sink(),
        continent=Sink(),
        country=Sink(),
        country_code=Sink(),
        country_language=Sink(),
        country_neighbor=Sink(),
        currency=Sink(),
        feature_class=Sink(),
        feature_code=Sink(),
        geoname=Sink(),
        hierarchy=Sink(),
        location=Sink(),
        language_code=Sink(),
        postal_code=Sink(),
        time_zone=Sink(),
        user_link=Sink(),
        user_tag=Sink(),
        wikidata=Sink(),

    ),
    sources=dict(
        alternate_name=Source(
            path='data/alt-names/alternateNamesV2.txt'
        ),
        continent=Source(

        ),
        country_info=Source(
            path='data/countryInfoClean.txt'
        ),
        feature_class=Source(),
        feature_code=Source(
            path='data/featureCodes_en.txt'
        ),
        geoname_all_countries=Source(
            path='data/allCountries.txt'
        ),
        geoname_no_country=Source(
            path='data/no-country.txt'
        ),
        hierarchy=Source(
            path='data/hierarchy.txt'
        ),
        iso_language=Source(
            path='data/iso-languagecodes.txt'
        ),
        shape=Source(
            path='data/shapes_all_low.txt'
        ),
        time_zone=Source(
            path='data/timeZones.txt'
        ),
        user_tag=Source(
            path='data/userTags.txt'
        ),
    )
)
