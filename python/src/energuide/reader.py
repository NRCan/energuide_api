import csv
import typing


InputData = typing.Dict[str, typing.Any]


class InvalidInputDataException(Exception):
    pass


def read(filename: str) -> typing.Iterator[InputData]:
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    current_group_value = None
    current_group: typing.List[InputData] = []

    for row in raw:
        this_group_value = row.get(grouping_field)
        if this_group_value is None:
            raise InvalidInputDataException(f'Grouper missing grouping field: {grouping_field}')

        if this_group_value == current_group_value:
            current_group.append(row)
        else:
            if current_group:
                yield current_group
                current_group = []
            current_group.append(row)
            current_group_value = this_group_value

    if current_group:
        yield current_group
