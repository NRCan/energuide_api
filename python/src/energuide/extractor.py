import csv
import itertools
import json
import cerberus
from energuide import reader, dwelling


class SerializableGenerator(list):
    def __init__(self, iterable):
        tmp_body = iter(iterable)
        try:
            self._head = iter([next(tmp_body)])
            self.append(tmp_body)
        except StopIteration:
            self._head = []

    def __iter__(self):
        return itertools.chain(self._head, *self[:1])




_SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in dwelling.EvaluationType]},

        'HOUSEREGION': {'type': 'integer', 'required': True},
        'WEATHERLOC': {'type': 'integer', 'required': True},
        'ENTRYBY': {'type': 'integer', 'required': True},
        'CLIENTCITY': {'type': 'integer', 'required': True},
        'CLIENTPCODE': {'type': 'integer', 'required': True},
        'CLIENTNAME': {'type': 'integer', 'required': True},
        'TELEPHONE': {'type': 'integer', 'required': True},
        'MAIL_CITY': {'type': 'integer', 'required': True},
        'MAIL_REGION': {'type': 'integer', 'required': True},
        'MAIL_PCODE': {'type': 'integer', 'required': True},
        'TAXNUMBER': {'type': 'integer', 'required': True},

        'RAW_XML': {'type': 'string', 'required': True}
    }

_DROP = ['HOUSEREGION',
         'WEATHERLOC',
         'ENTRYBY', 
         'CLIENTCITY',
         'CLIENTPCODE'
         'CLIENTNAME',
         'TELEPHONE', 
         'MAIL_CITY', 
         'MAIL_REGION'
         'MAIL_PCODE',
         'TAXNUMBER', 
         'RAW_XML']

def validated(it: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in reader:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')
        document = validator.document

        for key in _DROP:
            document.pop(key)

        yield document



def extract(infile: str) ->. typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    with open(infile, 'r') as csv_input, open(outfile, 'w') as json_output:
        reader = csv.DictReader(csv_input)
        return SerializableGenerator(blob for blob in validated(reader))
