"""
    geonames/readers
    ~~~~~~~~~~~~~~~~

    Contains reader implementations.
"""
import contextlib
import io
import os
import zipfile

from typing import IO


@contextlib.contextmanager
def text_reader(path: str) -> IO:
    with io.open(path, mode='r', encoding='utf-8') as f:
        yield f


@contextlib.contextmanager
def zip_reader(path: str) -> IO:
    filename = os.path.splitext(os.path.basename(path))[0]
    with zipfile.ZipFile(path) as zf:
        yield zf.open(filename, mode='r')
