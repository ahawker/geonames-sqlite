# geonames-sqlite

[GeoNames](http://www.geonames.org/) daily data dump as a [SQLite](https://www.sqlite.org/) database.

## Status

This repository is under active development.

## Usage

(Tested on python 3.7.3 only)

```python
$ python wip.py
```

## TODO

* [ ] Add proper CLI
* [ ] Refactor Options (defined in a few places) + JSON file serde
* [ ] Add Column/Index types that can be enabled/disabled
* [ ] Add file download/zip extraction
* [ ] Add common options patterns based on usage
* [ ] Add table/index size breakdown so users can determine where to get best savings

## License

The code in this repository is [Apache 2.0](LICENSE) licensed.

The GeoNames data is licensed under the [Creative Commons Attribution 3.0 License](http://creativecommons.org/licenses/by/3.0/).

## Attribution

This product uses includes/uses data offered by [GeoNames](http://www.geonames.org/).
