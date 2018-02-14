import itertools
import json
import typing
import zipfile


InputData = typing.Dict[str, typing.Any]


class InvalidInputDataException(Exception):
    pass


def read(filename: str) -> typing.Iterator[InputData]:
    with zipfile.ZipFile(filename) as zip_input:
        files = zip_input.namelist()
        for file in files:
            house = json.loads(zip_input.read(file))
            house['localFileName'] = file
            yield house


def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
