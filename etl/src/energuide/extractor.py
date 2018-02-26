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

KEEP_FIELDS = [
    'EVAL_ID',
    'EVAL_TYPE',
    'BUILDER',
    'DHWHPCOP',
    'ERSRATING',
    'ENTRYDATE',
    'CREATIONDATE',
    'MODIFICATIONDATE',
    'YEARBUILT',
    'CLIENTCITY',
    'HOUSEREGION',
]

REQUIRED_FIELDS = DROP_FIELDS + KEEP_FIELDS


_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}
_WINDOWS_LONG_SIZE = (2 ** 31) - 1


def _validated(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    validator = cerberus.Validator(_SCHEMA, purge_unknown=True)
    for row in data:
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise InvalidInputDataError(f'Validator failed on keys: {error_keys}')
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
        row['forwardSortationArea'] = row['CLIENTPCODE'][:3]

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

        yield row


def _remove_pii_fields(data: typing.Iterable[reader.InputData]) -> typing.Iterator[reader.InputData]:
    for row in data:
        for key in DROP_FIELDS:
            row.pop(key)
        yield row


def extract_data(input_path: str) -> typing.Iterator[reader.InputData]:
    data = _read_csv(input_path)
    validated_data = _validated(data)
    data_with_snippets = _extract_snippets(validated_data)
    safe_extract = _remove_pii_fields(data_with_snippets)
    return safe_extract


def write_data(data: typing.Iterable[reader.InputData], output_path: str) -> None:
    with zipfile.ZipFile(output_path, mode='w') as output_zip:
        for blob in data:
            blob_id = blob.get('BUILDER')
            if blob_id:
                output_zip.writestr(blob_id, json.dumps(blob))
