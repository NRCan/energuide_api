import csv
import itertools
import json
import typing
import sys
import cerberus
from energuide import reader


DROP_FIELDS = ['ENTRYBY',
               'CLIENTNAME',
               'CLIENTADDR',
               'CLIENTPCODE',
               'TELEPHONE',
               'MAIL_ADDR',
               'MAIL_PCODE',
               'TAXNUMBER',
               'RAW_XML']

REQUIRED_FIELDS = DROP_FIELDS + [
    'EVAL_ID',
    'EVAL_TYPE'
]

_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}


def _validated(data: typing.Iterable[reader.InputData], validator) -> typing.Iterator[reader.InputData]:
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        document = validator.document
        document['FORWARDSORTATIONAREA'] = document['CLIENTPCODE'][:3]
        for key in DROP_FIELDS:
            document.pop(key)

        yield document


def _read_csv(filepath: str) -> typing.Iterator[reader.InputData]:
    csv.field_size_limit(sys.maxsize)
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def extract_data(input_path: str) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    return _validated(_read_csv(input_path), validator)


class _SerializableGenerator(list):

    def __init__(self, iterable):
        super().__init__()
        tmp_body = iter(iterable)
        try:
            self._head = iter([next(tmp_body)])
            self.append(tmp_body)
        except StopIteration:
            self._head = []

    def __iter__(self):
        return itertools.chain(self._head, *self[:1])


def write_data(data: typing.Iterable[reader.InputData], output_path: str) -> None:
    output_data = _SerializableGenerator(data)
    with open(output_path, 'w') as output_file:
        json.dump(output_data, output_file)
