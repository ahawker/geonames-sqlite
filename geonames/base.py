"""
    geonames/base
    ~~~~~~~~~~~~~

    Contains abstract/base types.
"""
import abc
import csv
import io

from geonames import fileutils, validators
from pydantic import BaseModel, validator
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Type, TypeVar

from . import options


class Record(BaseModel):
    """
    Base class for all record types.
    """
    _empty_string_to_none = validator('*', allow_reuse=True, pre=True)(validators.empty_str_to_none)


RecordT = TypeVar('RecordT', bound=Record)


class Source(metaclass=abc.ABCMeta):
    """
    Abstract class for a data source.
    """
    def __init__(self,
                 name: str,
                 record_cls: Type[RecordT]) -> None:
        self.name = name
        self.record_cls = record_cls

    @abc.abstractmethod
    def produce(self, *args) -> Iterator[RecordT]:
        """
        Produce record instances from the source.
        """


class FileSource(Source):
    """
    Data source for line-based column delimited files.
    """
    def __init__(self,
                 name: str,
                 record_cls: Type[RecordT],
                 fields: List[str],
                 delimiter: str = '\t',
                 skip_header: bool = False,
                 skip_comments: bool = False,
                 field_size_limit: Optional[int] = None):
        super().__init__(name, record_cls)
        self.fields = fields
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_comments = skip_comments
        self.field_size_limit = field_size_limit

    def produce(self, opts: options.Source) -> Iterator[RecordT]:
        """
        Read the given file and produce a record instance for each line.
        """
        with io.open(opts.path, encoding='utf-8') as f:
            if self.skip_header:
                next(f)
            if self.skip_comments:
                fileutils.skip_comments(f)
            if self.field_size_limit:
                prev_limit = csv.field_size_limit(self.field_size_limit)

            reader = csv.DictReader(f, fieldnames=self.fields, delimiter=self.delimiter)

            for i, row in enumerate(reader):
                yield self.record_cls(row_num=i + 1, **row)

            if self.field_size_limit:
                csv.field_size_limit(prev_limit)


class ListSource(Source):
    """
    Data source for in-memory list of dicts.
    """
    def __init__(self,
                 name: str,
                 record_cls: Type[RecordT],
                 dataset: List[Dict[str, Any]]):
        super().__init__(name, record_cls)
        self.dataset = dataset

    def produce(self, *args) -> Iterator[RecordT]:
        """
        Produce a record instance from each entry in the dataset.
        """
        for i, row in enumerate(self.dataset):
            yield self.record_cls(row_num=i + 1, **row)


SourceT = TypeVar('SourceT', bound=Source)

TableT = TypeVar('TableT')

T = TypeVar('T')


class Sink(Generic[T], metaclass=abc.ABCMeta):
    """
    Abstract data sink.
    """
    def __init__(self,
                 name: str,
                 table: TableT,
                 predicate: Optional[Callable[[T], bool]] = None,
                 exception_handler: Optional[Callable[[Any, Any, T, Exception], bool]] = None):
        self.name = name
        self.table = table
        self.predicate = predicate
        self.exception_handler = exception_handler

    @abc.abstractmethod
    def consume_record(self, db, opts: options.Sink, record: T) -> None:
        """
        Consume an individual data source record that meets our
        optional predicate requirements.
        """

    def consume(self, db, opts: options.Sink, record: T) -> None:
        """
        Consume an individual data source record and conditionally consume it.
        """
        if not opts.enabled:
            return
        if self.predicate and not self.predicate(record):
            return

        try:
            return self.consume_record(db, opts, record)
        except Exception as ex:
            if not self.exception_handler:
                raise ex

            handled = self.exception_handler(db, options, record, ex)
            if not handled:
                raise ex

    def pre_consume(self, db, opts: options.Sink) -> None:
        """
        Configure any necessary state prior to consuming data source records.
        """
        if opts.enabled:
            self.table.create_table(db)
            self.table.create_indices(db)

    def post_consume(self, db, opts: options.Sink) -> None:
        """
        Teardown any necessary state after consuming all data source records.
        """
        if opts.enabled:
            self.table.commit(db)

    def checkpoint(self, db, opts: options.Sink) -> None:
        """
        Save partial process of data source records already consumed.
        """
        if opts.enabled:
            self.table.commit(db)


SinkT = TypeVar('SinkT', bound=Sink)


class RecordSink(Sink[T]):
    """
    Data sink for individual data source records.
    """
    def __init__(self,
                 name: str,
                 table: TableT,
                 predicate: Optional[Callable[[T], bool]] = None,
                 exception_handler: Optional[Callable[[Any, Any, T, Exception], bool]] = None,
                 transform: Optional[Callable[[T], Dict[str, Any]]] = None):
        super().__init__(name, table, predicate, exception_handler)
        self.transform = transform

    def consume_record(self, db, options, record: T) -> None:
        """
        Consume a record generated by a source and conditionally apply it to our table.
        """
        params = self.transform(record)
        return self.table.apply(db, params)


class FlattenRecordFieldSink(Sink[T]):
    """
    Data sink for flattening data source record fields that are iterables.
    TODO - Transform type hint needs to record and varargs (otional tuple any?)
    """
    def __init__(self,
                 name: str,
                 table: TableT,
                 field_name: str,
                 field_predicate: Optional[Callable[[T, Any], bool]] = None,
                 predicate: Optional[Callable[[T], bool]] = None,
                 exception_handler: Optional[Callable[[Any, Any, T, Exception], bool]] = None,
                 transform: Optional[Callable[[T, Any, int], Dict[str, Any]]] = None):
        super().__init__(name, table, predicate, exception_handler)
        self.transform = transform
        self.field_name = field_name
        self.field_predicate = field_predicate

    def consume_record(self, db, opts: options.Sink, record: T) -> None:
        """
        Consume a record generated by a source and conditionally apply it to our table.
        """
        for i, value in enumerate(getattr(record, self.field_name, [])):
            if self.field_predicate and not self.field_predicate(record, value):
                continue
            params = self.transform(record, value, i)
            return self.table.apply(db, params)


class Table:
    """
    Represents a sqlite database table.
    """
    def __init__(self,
                 name: str,
                 table: Optional[str],
                 indices: Optional[str],
                 modify: str) -> None:
        self.name = name
        self.table = table
        self.indices = indices
        self.modify = modify

    def create_table(self, db):
        """
        Create a sqlite table (if we have one defined).
        """
        if self.table:
            return db.executescript(self.table)

    def create_indices(self, db):
        """
        Create one or more sqlite indices (if we have any defined).
        """
        if self.indices:
            return db.executescript(self.indices)

    @staticmethod
    def commit(db):
        """
        Commit any outstanding database modifications.
        """
        return db.commit()

    def apply(self, db, params) -> None:
        """
        Apply changes to a sqlite table (if we have any defined).
        """
        return db.execute(self.modify, params)


class Pipeline:
    """
    Data pipeline to feed data source records from one Source to one or more Sinks.
    """
    def __init__(self,
                 source: SourceT,
                 sinks: List[SinkT],
                 checkpoint_threshold: Optional[int] = 100000):
        self.source = source
        self.sinks = sinks
        self.checkpoint_threshold = checkpoint_threshold

    def __str__(self):
        return f'{self.source.name} -> {[s.name for s in self.sinks]}'

    def run(self, db, opts: options.Pipeline):
        """
        Consume the source and feed records to all configured sinks.
        """
        source_options = opts.sources[self.source.name]
        sink_options = [opts.sinks[sink.name] for sink in self.sinks]

        for i, sink in enumerate(self.sinks):
            sink.pre_consume(db, sink_options[i])

        for record in self.source.produce(source_options):
            for i, sink in enumerate(self.sinks):
                sink.consume(db, sink_options[i], record)

                if record.row_num % self.checkpoint_threshold == 0:
                    print(f'Checkpoint {sink.name} @ {record.row_num}')
                    sink.checkpoint(db, sink_options[i])

        for i, sink in enumerate(self.sinks):
            sink.post_consume(db, sink_options[i])


class PipelineGraph:
    """
    Represents the order/dependency graph of pipelines.
    """
    def __init__(self, pipelines):
        self.pipelines = pipelines

    def run(self, db, opts: options.Pipeline):
        for pipeline in self.pipelines:
            print(f'Starting pipeline {pipeline}')
            pipeline.run(db, opts)
            print(f'Finished pipeline {pipeline}')
