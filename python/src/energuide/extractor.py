import csv
import typing
import sys
import cerberus
from energuide import reader


_SCHEMA = {
    'EVAL_ID': {'type': 'string', 'required': True},
    'EVAL_TYPE': {'type': 'string', 'required': True},

    'ENTRYBY': {'type': 'string', 'required': True},
    'CLIENTPCODE': {'type': 'string', 'required': True},
    'CLIENTNAME': {'type': 'string', 'required': True},
    'TELEPHONE': {'type': 'string', 'required': True},
    'MAIL_PCODE': {'type': 'string', 'required': True},
    'TAXNUMBER': {'type': 'string', 'required': True},

    'RAW_XML': {'type': 'string', 'required': True}
    }

DROP_FIELDS = ['ENTRYBY',
               'CLIENTNAME',
               'CLIENTPCODE',
               'TELEPHONE',
               'MAIL_PCODE',
               'TAXNUMBER',
               'RAW_XML']


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
