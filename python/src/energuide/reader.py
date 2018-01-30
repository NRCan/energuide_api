import csv
import json
import itertools
import sys
import typing


InputData = typing.Dict[str, typing.Any]
                

class InvalidInputDataException(Exception):
    pass


_SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in EvaluationType]},
        'ENTRYDATE': {'type': 'string', 'required': True},
        'CREATIONDATE': {'type': 'string', 'required': True},
        'MODIFICATIONDATE': {'type': 'string', 'required': True},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'CLIENTPCODE': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z] [0-9][A-Z][0-9]'},
        'HOUSEREGION': {'type': 'string', 'required': True},
    }



def read(filename: str) -> typing.Iterator[InputData]:
    csv.field_size_limit(sys.maxsize)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

def extract_xml(xml: str):
    return {'testfield': 0}


def extract(infile: str, outfile: str):
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    input_data = read(infile)
    with open(outfile, 'w') as output:
        writer = csv.DictWriter(output, fieldnames)
        for row in input_data:
            xml = row.pop('xml')


            writer.writerow()



def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
