"""
    wip
    ~~~

    Simply "WIP" entrypoint for testing geonames-sqlite creation.
"""
import sqlite3

from geonames import options, pipelines


def main():
    db = sqlite3.connect('geonames-wip.sqlite')
    db.execute('PRAGMA foreign_keys = ON;')
    db.execute('PRAGMA synchronous = OFF;')
    db.execute('PRAGMA journal_mode = MEMORY;')
    db.execute('PRAGMA page_size = 4096;')

    pipelines.Graph.run(db, options.Graph)

    db.execute('VACUUM;')


if __name__ == '__main__':
    main()
