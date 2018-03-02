import itertools
import json
import os
import typing
import zipfile
from azure.storage import blob
from energuide import dwelling
from energuide import logging
from energuide.exceptions import InvalidEmbeddedDataTypeError
from energuide.exceptions import EnerguideError


LOGGER = logging.get_logger(__name__)


class AzureCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


def _read_local(zip_filename: str) -> typing.Iterator[bytes]:
    with zipfile.ZipFile(zip_filename) as zip_input:
        for file in zip_input.namelist():
            yield zip_input.read(file)


def _read_azure(coords: AzureCoordinates) -> typing.Iterator[bytes]:
    azure_service = blob.BlockBlobService(account_name=coords.account,
                                          account_key=coords.key,
                                          custom_domain=coords.domain)

    # itertools.groupby() needs its input sorted by the groupby key. We are assuming that that key is the filename
    files = sorted([blob_.name for blob_ in azure_service.list_blobs(coords.container)
                    if 'timestamp' not in blob_.name])
    for file in files:
        yield azure_service.get_blob_to_bytes(coords.container, file).content


def _read(reader: typing.Iterable[bytes]) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    for content in reader:
        house = json.loads(content)
        house['jsonFileName'] = content
        yield house


def _read_groups(reader: typing.Iterable[bytes]) -> typing.Iterator[typing.List[typing.Dict[str, typing.Any]]]:
    for group in itertools.groupby(_read(reader), lambda y: y.get(dwelling.Dwelling.GROUPING_FIELD)):
        yield [x for x in group[1]]


def _generate_dwellings(grouped: typing.List[typing.Dict[str, typing.Any]]) -> typing.Optional[dwelling.Dwelling]:
    try:
        return dwelling.Dwelling.from_group(grouped)
    except InvalidEmbeddedDataTypeError as exc:
        files = [str(file.get('jsonFileName')) for file in grouped]
        failing_type = exc.data_class
        LOGGER.error(f'Files: "{", ".join(files)}": {failing_type.__name__}')
    except EnerguideError as exc:
        files = [str(file.get('jsonFileName')) for file in grouped]
        LOGGER.error(f'Files: "{", ".join(files)}" - {exc}')
    return None


def transform(azure: bool, filename: typing.Optional[str]) -> typing.Iterator[dwelling.Dwelling]:
    if azure:
        azure_coordinates = AzureCoordinates(
            account=os.environ.get('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', ''),
            key=os.environ.get('EXTRACT_ENDPOINT_STORAGE_KEY', ''),
            container=os.environ.get('EXTRACT_ENDPOINT_CONTAINER', ''),
            domain=os.environ.get('EXTRACT_ENDPOINT_STORAGE_DOMAIN', None)
        )
        data_reader = _read_azure(azure_coordinates)
    elif filename:
        data_reader = _read_local(filename)
    else:
        raise ValueError("must supply a filename if not using Azure")

    for row_group in _read_groups(data_reader):
        output = _generate_dwellings(row_group)
        if output:
            yield output
