import csv
import json
import typing
import sys
import zipfile
import cerberus
from energuide import element
from energuide import reader
from energuide import snippets
from energuide.exceptions import InvalidInputDataError


REQUIRED_FIELDS = [
    'EVAL_ID',
    'EVAL_TYPE',
    'BUILDER',
    'ENTRYDATE',
    'CREATIONDATE',
    'MODIFICATIONDATE',
    'YEARBUILT',
    'CLIENTCITY',
    'HOUSEREGION',
    'RAW_XML',
]

NULLABLE_FIELDS = ['MODIFICATIONDATE']

INPUT_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}
for field in NULLABLE_FIELDS:
    INPUT_SCHEMA[field] = {'type': 'string', 'required': True, 'nullable': True}

_WINDOWS_LONG_SIZE = (2 ** 31) - 1


def _empty_to_none(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        for key, value in row.items():
            if value == '':
                row[key] = None
        yield row


def _validated(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(INPUT_SCHEMA, purge_unknown=True)
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise InvalidInputDataError(f'Validator failed on keys: {error_keys} for {row.get("BUILDER")}')
        yield validator.document


def _read_csv(filepath: str) -> typing.Iterator[reader.InputData]:
    try:
        csv.field_size_limit(sys.maxsize)
    except OverflowError:
        csv.field_size_limit(_WINDOWS_LONG_SIZE)

    with open(filepath, 'r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def _safe_merge(data: reader.InputData, extra: reader.InputData) -> reader.InputData:
    for key, value in extra.items():
        assert key not in data
        data[key] = value
    return data


def _extract_snippets(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        doc = element.Element.from_string(row['RAW_XML'])
        house_node = doc.xpath('House')
        if house_node:
            house_snippets = snippets.snip_house(house_node[0])
            row = _safe_merge(row, house_snippets.to_dict())

        code_node = doc.xpath('Codes')
        if code_node:
            code_snippets = snippets.snip_codes(code_node[0])
            row = _safe_merge(row, code_snippets.to_dict())

        upgrades_node = doc.xpath('EnergyUpgrades')
        if upgrades_node:
            energy_snippets = snippets.snip_energy_upgrades(upgrades_node[0])
            row = _safe_merge(row, energy_snippets.to_dict())

        tsv_fields = snippets.snip_tsv(doc)
        row = _safe_merge(row, tsv_fields.to_dict())
        yield row


def extract_data(input_path: str) -> typing.Iterator[reader.InputData]:
    data = _read_csv(input_path)
    patched = _empty_to_none(data)
    validated_data = _validated(patched)
    return _extract_snippets(validated_data)


def write_data(data: typing.Iterable[reader.InputData], output_path: str) -> None:
    with zipfile.ZipFile(output_path, mode='w') as output_zip:
        for blob in data:
            blob_id = blob.get('BUILDER')
            if blob_id:
                output_zip.writestr(blob_id, json.dumps(blob))
