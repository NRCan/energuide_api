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


def extract(csv_input: typing.Iterable[str]) -> typing.Iterator[reader.InputData]:
    csv.field_size_limit(sys.maxsize)

    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    csv_reader = csv.DictReader(csv_input)
    for blob in validated(csv_reader, validator):
        yield blob
