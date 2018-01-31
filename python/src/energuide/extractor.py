import csv
import typing
import sys
import cerberus
from energuide import reader


REQUIRED_FIELDS = [
    'EVAL_ID',
    'EVAL_TYPE',
    'ENTRYBY',
    'CLIENTPCODE',
    'CLIENTNAME',
    'TELEPHONE',
    'MAIL_ADDR',
    'MAIL_PCODE',
    'TAXNUMBER',
    'CLIENTADDR',
    'RAW_XML'
]

DROP_FIELDS = ['ENTRYBY',
               'CLIENTNAME',
               'CLIENTADDR',
               'CLIENTPCODE',
               'TELEPHONE',
               'MAIL_ADDR',
               'MAIL_PCODE',
               'TAXNUMBER',
               'RAW_XML']

_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}


def validated(data: typing.Iterable[reader.InputData], validator) -> typing.Iterator[reader.InputData]:
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        document = validator.document
        document['FORWARDSORTATIONAREA'] = document['CLIENTPCODE'][:3]
        for key in DROP_FIELDS:
            document.pop(key)

        yield document


def _read_csv(filepath: str):
    csv.field_size_limit(sys.maxsize)
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def extract(filepath: str) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)

    for blob in validated(_read_csv(filepath), validator):
        yield blob
