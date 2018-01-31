import csv
import itertools
import json
import sys
import typing
import zipfile


InputData = typing.Dict[str, typing.Any]


class InvalidInputDataException(Exception):
    pass


def zip_read(filename: str) -> typing.Iterator[InputData]:
    with zipfile.ZipFile(filename) as zip_input:
        files = zip_input.namelist()
        for file in files:
            yield json.loads(zip_input.read(file))


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
