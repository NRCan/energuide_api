import csv
import itertools
import typing
import sys
import cerberus
from energuide import reader, dwelling


_SCHEMA = {
        'EVAL_ID': {'type': 'string', 'required': True},
        'EVAL_TYPE': {'type': 'string', 'required': True},

        'HOUSEREGION': {'type': 'string', 'required': True},
        'WEATHERLOC': {'type': 'string', 'required': True},
        'ENTRYBY': {'type': 'string', 'required': True},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'CLIENTPCODE': {'type': 'string', 'required': True},
        'CLIENTNAME': {'type': 'string', 'required': True},
        'TELEPHONE': {'type': 'string', 'required': True},
        'MAIL_CITY': {'type': 'string', 'required': True},
        'MAIL_REGION': {'type': 'string', 'required': True},
        'MAIL_PCODE': {'type': 'string', 'required': True},
        'TAXNUMBER': {'type': 'string', 'required': True},

        'RAW_XML': {'type': 'string', 'required': True}
    }

DROP_FIELDS = ['HOUSEREGION',
         'WEATHERLOC',
         'ENTRYBY', 
         'CLIENTCITY',
         'CLIENTPCODE',
         'CLIENTNAME',
         'TELEPHONE', 
         'MAIL_CITY', 
         'MAIL_REGION',
         'MAIL_PCODE',
         'TAXNUMBER', 
         'RAW_XML']


def validated(it: typing.Iterable[reader.InputData], validator) -> typing.Iterator[reader.InputData]:
    for row in it:
        if not validator.validate(row):
            import pdb; pdb.set_trace()
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        document = validator.document

        for key in DROP_FIELDS:
            document.pop(key)

        yield document


def extract(csv_input: str) -> typing.Iterator[reader.InputData]:
    csv.field_size_limit(sys.maxsize)

    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    reader = csv.DictReader(csv_input)
    for blob in validated(reader, validator):
        yield blob
