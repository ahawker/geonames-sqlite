"""
    geonames/validation
    ~~~~~~~~~~~~~~~~~~~

    Contains reusable pydantic validators.
"""
from typing import List, Optional


def empty_str_to_none(value: str) -> Optional[str]:
    return None if value == '' else value


def zero_to_none(value: int) -> Optional[int]:
    return None if value == 0 else value


def sentinel_to_none(value: str, sentinel: str) -> Optional[int]:
    return None if value == sentinel else int(value)


def optional_int_to_bool(value: str) -> bool:
    return bool(int(value)) if value else False


def csv_str_to_list(value: str, delimiter: str = ',') -> Optional[List[str]]:
    return None if not value else [v for v in value.split(delimiter) if v]
