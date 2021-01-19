"""
    geonames/fileutils
    ~~~~~~~~~~~~~~~~~~

    Contains utility functions for files.
"""
from typing import IO


def peek_line(f: IO) -> str:
    """
    Peek the next line of the given file obj without progressing the pointer.
    """
    pos = f.tell()
    data = f.readline()
    f.seek(pos)
    return data


def is_comment(line: str) -> bool:
    """
    Return True if the given line is a comment, False otherwise.
    """
    return line.startswith('#')


def skip_comments(f: IO) -> None:
    """
    Progress the given file obj past all comment lines.
    """
    while True:
        line = peek_line(f)
        if not line or not is_comment(line):
            break
        f.readline()
