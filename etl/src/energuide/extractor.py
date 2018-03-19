import csv
import json
import typing
import sys
import zipfile
import cerberus
from tqdm import tqdm
from energuide import element
from energuide import logger
from energuide import snippets
from energuide.exceptions import InvalidInputDataError, EnerguideError


LOGGER = logger.get_logger(__name__)


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


def _empty_to_none(row: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    for key, value in row.items():
        if value == '':
            row[key] = None
    return row


def _validated(row: typing.Dict[str, typing.Any], validator: cerberus.Validator) -> typing.Dict[str, typing.Any]:
    if not validator.validate(row):
        error_keys = ', '.join(validator.errors.keys())
        raise InvalidInputDataError(f'Validator failed on keys: {error_keys} for {row.get("BUILDER")}')
    return validator.document


def _read_csv(filepath: str, show_progress: bool) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    try:
        csv.field_size_limit(sys.maxsize)
    except OverflowError:
        csv.field_size_limit(_WINDOWS_LONG_SIZE)

    with open(filepath, 'r', encoding='utf-8', newline='') as file:
        total_lines = sum(1 for _ in file)

    with tqdm(open(filepath, 'r', encoding='utf-8', newline=''),
              total=total_lines, unit=' lines', disable=not show_progress) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def _safe_merge(data: typing.Dict[str, typing.Any],
                extra: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    for key, value in extra.items():
        assert key not in data
        data[key] = value
    return data


def _extract_snippets(row: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    doc = element.Element.from_string(row['RAW_XML'])
    house_node = doc.xpath('House')
    if house_node:
        house_snippets = snippets.snip_house(house_node[0])
        row = _safe_merge(row, house_snippets.to_dict())
    else:
        row = _safe_merge(row, snippets.HouseSnippet.EMPTY_SNIPPET)

    code_node = doc.xpath('Codes')
    if code_node:
        code_snippets = snippets.snip_codes(code_node[0])
        row = _safe_merge(row, code_snippets.to_dict())
    else:
        row = _safe_merge(row, snippets.Codes.EMPTY_SNIPPET)

    upgrades_node = doc.xpath('EnergyUpgrades')
    if upgrades_node:
        energy_snippets = snippets.snip_energy_upgrades(upgrades_node[0])
        row = _safe_merge(row, energy_snippets.to_dict())
    else:
        row = _safe_merge(row, snippets.EnergyUpgradesSnippet.EMPTY_SNIPPET)

    tsv_fields = snippets.snip_other_data(doc)
    row = _safe_merge(row, tsv_fields.to_dict())
    return row


def extract_data(input_path: str,
                 show_progress: bool = False) -> typing.Iterator[typing.Optional[typing.Dict[str, typing.Any]]]:
    validator = cerberus.Validator(INPUT_SCHEMA, purge_unknown=True)
    rows = _read_csv(input_path, show_progress)

    for row in rows:
        try:
            patched = _empty_to_none(row)
            validated_data = _validated(patched, validator)
            result = _extract_snippets(validated_data)
            yield result
        except EnerguideError as ex:
            LOGGER.error(f"Error extracting data from row {row.get('BUILDER', 'Unknown ID')}. Details: {ex}")
            yield None


def write_data(data: typing.Iterable[typing.Optional[typing.Dict[str, typing.Any]]],
               output_path: str) -> typing.Tuple[int, int]:
    records_written, records_failed = 0, 0
    with zipfile.ZipFile(output_path, mode='w', compression=zipfile.ZIP_DEFLATED) as output_zip:
        for blob in data:
            if blob is None or not blob.get('BUILDER'):
                records_failed += 1
            else:
                blob_id: str = blob['BUILDER']
                eval_id: str = blob['EVAL_ID']
                output_zip.writestr(f'{eval_id}-{blob_id}', json.dumps(blob))
                records_written += 1

    return records_written, records_failed
