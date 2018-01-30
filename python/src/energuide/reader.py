import csv
import json
import itertools
import sys
import typing


InputData = typing.Dict[str, typing.Any]
                

class InvalidInputDataException(Exception):
    pass


def read(filename: str) -> typing.Iterator[InputData]:
    csv.field_size_limit(sys.maxsize)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
