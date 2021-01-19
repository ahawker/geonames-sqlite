"""
    geonames/exceptions
    ~~~~~~~~~~~~~~~~~~~
"""
from . import base


def ignore_foreign_key_constraint(db, options, record: base.T, exception: Exception) -> bool:
    return 'FOREIGN KEY constraint failed' in str(exception)


def ignore_unique_key_constraint(db, options, record: base.T, exception: Exception) -> bool:
    return 'UNIQUE constraint failed' in str(exception)
