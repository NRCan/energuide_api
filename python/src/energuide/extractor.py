import csv
import json
import cerberus
from energuide import reader, dwelling

# TODO reference schema from somewhere else, possibly dwelling.ParsedDwellingDataRow
_SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in dwelling.EvaluationType]},
        'ENTRYDATE': {'type': 'string', 'required': True},
        'CREATIONDATE': {'type': 'string', 'required': True},
        'MODIFICATIONDATE': {'type': 'string', 'required': True},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'CLIENTPCODE': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z] [0-9][A-Z][0-9]'},
        'HOUSEREGION': {'type': 'string', 'required': True},
    }

_fields = _SCHEMA.keys()


def extract(infile: str, outfile: str):
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True, purge_unknown=True)
    with open(infile, 'r') as csv_input, open(outfile, 'w') as csv_output:
        reader = csv.DictReader(csv_input)
        writer = csv.DictWriter(csv_output, fieldnames=[field for field in reader.fieldnames if field in _fields])

        out = (blob for blob in (validator.validated(row) for row in input_data)
               if blob is not None)
        json.dump(out)
