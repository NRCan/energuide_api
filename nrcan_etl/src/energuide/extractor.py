import csv
import json
import typing
import sys
import zipfile
import cerberus
from tqdm import tqdm
from energuide import logger
from energuide import element
from energuide import snippets
from energuide.exceptions import InvalidInputDataError
from energuide.exceptions import EnerguideError


LOGGER = logger.get_logger(__name__)


REQUIRED_FIELDS = [
    'EVAL_ID',
    'EVAL_TYPE',
    'BUILDER',
    'ENTRYDATE',
    'CREATIONDATE',
    'YEARBUILT',
    'CLIENTCITY',
    'HOUSEREGION',
    'HOUSE_ID',
]

NULLABLE_FIELDS = [
    'MODIFICATIONDATE',
    'forwardSortationArea',
    'HEATEDFLOORAREA',
    'TYPEOFHOUSE',
    'ERSRATING',
    'UGRERSRATING',
    'EGHRATING',
    'UGRRATING',
    'ERSGHG',
    'UGRERSGHG',
    'ERSENERGYINTENSITY',
    'UGRERSENERGYINTENSITY',
    'EGHDESHTLOSS',
    'UGRDESHTLOSS',
    'WALLDEF',
    'UGRWALLDEF',
    'EGHHLWALLS',
    'UGRHLWALLS',
]

INPUT_SCHEMA = {field: {'type': 'string', 'required': True} for field in REQUIRED_FIELDS}
for field in NULLABLE_FIELDS:
    INPUT_SCHEMA[field] = {'type': 'string', 'required': True, 'nullable': True}

INPUT_SCHEMA['RAW_XML'] = {'type': 'string', 'required': False, 'nullable': True}
INPUT_SCHEMA['upgrades'] = {
    'type': 'list',
    'required': True,
    'nullable': True,
    'schema': {
        'type': 'string'
    }
}


_WINDOWS_LONG_SIZE = (2 ** 31) - 1


def _empty_to_none(row: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    for key, value in row.items():
        if value == '':
            row[key] = None
    return row


def _validated(
        row: typing.Dict[str, typing.Any],
        validator: cerberus.Validator) -> typing.Dict[str, typing.Optional[str]]:
    if not validator.validate(row):
        error_keys = ', '.join(validator.errors.keys())
        raise InvalidInputDataError(f'Validator failed on keys: {error_keys} for {row.get("BUILDER")}')
    return validator.document


def _truncate_postal_code(row: typing.Dict[str, typing.Optional[str]]) -> typing.Dict[str, typing.Optional[str]]:
    postal = row.get('MAIL_PCODE')
    row['forwardSortationArea'] = postal[0:3] if postal else None
    return row


def _safe_merge(data: typing.Dict[str, typing.Any],
                extra: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    for key, value in extra.items():
        assert key not in data
        data[key] = value
    return data


def _snip_upgrade_order(row: typing.Dict[str, typing.Optional[str]]) -> typing.Dict[str, typing.Optional[str]]:
    if row.get('RAW_XML'):
        xml = typing.cast(str, row['RAW_XML'])

        doc = element.Element.from_string(xml)
        upgrade_order = snippets.snip_energy_upgrade_order(doc)
        _safe_merge(row, upgrade_order.to_dict())
    else:
        _safe_merge(row, snippets.EnergyUpgradesSnippet.EMPTY_SNIPPET)

    return row


def _drop_unwanted(row: typing.Dict[str, typing.Optional[str]]) -> typing.Dict[str, typing.Optional[str]]:
    row.pop("RAW_XML", None)
    return row


def _read_csv(filepath: str, show_progress: bool) -> typing.Iterator[typing.Dict[str, str]]:
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


def extract_data(input_path: str,
                 show_progress: bool = False) -> typing.Iterator[typing.Optional[typing.Dict[str, typing.Any]]]:
    validator = cerberus.Validator(INPUT_SCHEMA, purge_unknown=True)
    rows = _read_csv(input_path, show_progress)

    for row in rows:
        try:
            patched = _empty_to_none(row)
            filtered = _truncate_postal_code(patched)
            ordered = _snip_upgrade_order(filtered)
            validated_data = _validated(ordered, validator)
            cleaned = _drop_unwanted(validated_data)
            yield cleaned
        except EnerguideError as ex:
            LOGGER.error(f"Error extracting data from row {row.get('BUILDER', 'Unknown ID')}. Details: {ex}")
            yield None


def write_data(data: typing.Iterable[typing.Optional[typing.Dict[str, typing.Any]]],
               output_path: str) -> typing.Tuple[int, int]:
    records_written, records_failed = 0, 0
    with zipfile.ZipFile(output_path, mode='w', compression=zipfile.ZIP_DEFLATED) as output_zip:
        for blob in data:
            if blob is None or not all((blob.get('BUILDER'), blob.get('EVAL_ID'), blob.get('HOUSE_ID'))):
                records_failed += 1
            else:
                blob_id = blob.get('BUILDER')
                eval_id = blob.get('EVAL_ID')
                house_id = blob.get('HOUSE_ID')
                output_zip.writestr(f'{house_id}-{eval_id}-{blob_id}', json.dumps(blob))
                records_written += 1

    return records_written, records_failed
