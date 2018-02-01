import csv
import json
import typing
from xml.etree import ElementTree
import sys
import zipfile
import cerberus
from energuide import reader
from energuide import snippets


DROP_FIELDS = ['ENTRYBY',
               'CLIENTNAME',
               'CLIENTADDR',
               'CLIENTPCODE',
               'TELEPHONE',
               'MAIL_ADDR',
               'MAIL_PCODE',
               'TAXNUMBER',
               'RAW_XML',
               'INFO1',
               'INFO2',
               'INFO3',
               'INFO4',
               'INFO5',
               'INFO6',
               'INFO7',
               'INFO8',
               'INFO9',
               'INFO10']

REQUIRED_FIELDS = DROP_FIELDS + [
    'EVAL_ID',
    'EVAL_TYPE',
    'BUILDER'
]

_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}


def _validated(data: typing.Iterable[reader.InputData], validator) -> typing.Iterator[reader.InputData]:
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')
        yield row


def _read_csv(filepath: str) -> typing.Iterator[reader.InputData]:
    csv.field_size_limit(sys.maxsize)
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def _extract_snippets(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        row['forwardSortationArea'] = row['CLIENTPCODE'][:3]

        doc = ElementTree.fromstring(row['RAW_XML'])
        house = doc.find('House')
        if house:
            extra_data = snippets.snip_house(house)

            for key, value in extra_data.items():
                assert key not in row
                row[key] = value

        yield row


def _remove_pii_fields(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        for key in DROP_FIELDS:
            row.pop(key)
        yield row


def extract_data(input_path: str) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, allow_unknown=True)
    data = _read_csv(input_path)
    validated_data = _validated(data, validator)
    data_with_snippets = _extract_snippets(validated_data)
    safe_extract = _remove_pii_fields(data_with_snippets)
    return safe_extract


def write_data(data: typing.Iterable[reader.InputData], output_path: str) -> None:
    with zipfile.ZipFile(output_path, mode='w') as output_zip:
        for blob in data:
            blob_id = blob.get('BUILDER')
            if blob_id:
                output_zip.writestr(blob_id, json.dumps(blob))
