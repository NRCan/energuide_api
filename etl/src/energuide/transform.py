import itertools
import json
import os
import typing
import zipfile
from tqdm import tqdm
import typing_extensions
from azure.storage import blob
from energuide import dwelling
from energuide import logger
from energuide.exceptions import InvalidEmbeddedDataTypeError
from energuide.exceptions import EnerguideError


LOGGER = logger.get_logger(__name__)


class _AzureCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


class AzureCoordinates(_AzureCoordinates):
    @classmethod
    def from_env(cls) -> 'AzureCoordinates':
        return AzureCoordinates(
            account=os.environ.get('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', ''),
            key=os.environ.get('EXTRACT_ENDPOINT_STORAGE_KEY', ''),
            container=os.environ.get('EXTRACT_ENDPOINT_CONTAINER', ''),
            domain=os.environ.get('EXTRACT_ENDPOINT_STORAGE_DOMAIN', None)
        )


class ExtractProtocol(typing_extensions.Protocol):
    def extracted_rows(self) -> typing.Iterator[typing.Dict[str, typing.Any]]:
        pass

    def num_rows(self) -> int:
        pass


class LocalExtractReader:

    def __init__(self, zip_filename: str) -> None:
        self._zip_filename = zip_filename

    def extracted_rows(self) -> typing.Iterator[typing.Dict[str, typing.Any]]:
        with zipfile.ZipFile(self._zip_filename) as zip_input:
            for file in zip_input.namelist():
                content = zip_input.read(file)
                house = json.loads(content)
                house['jsonFileName'] = file
                yield house

    def num_rows(self) -> int:
        with zipfile.ZipFile(self._zip_filename) as zip_input:
            return len(zip_input.namelist())


class AzureExtractReader:

    def __init__(self, coords: AzureCoordinates) -> None:
        self._coords = coords
        self._azure: typing.Optional[blob.BlockBlobService] = None

    @property
    def _azure_service(self) -> blob.BlockBlobService:
        if self._azure is None:
            self._azure = blob.BlockBlobService(account_name=self._coords.account,
                                                account_key=self._coords.key,
                                                custom_domain=self._coords.domain)
        return self._azure

    def _files(self) -> typing.List[str]:
        # itertools.groupby() needs its input sorted by the groupby key. We are assuming that that key is the filename
        files = sorted([blob_.name for blob_ in self._azure_service.list_blobs(self._coords.container)
                        if 'timestamp' not in blob_.name])
        return files

    def extracted_rows(self) -> typing.Iterator[typing.Dict[str, typing.Any]]:
        for file in self._files():
            content = self._azure_service.get_blob_to_bytes(self._coords.container, file).content
            house = json.loads(content)
            house['jsonFileName'] = file
            yield house

    def num_rows(self) -> int:
        return len(self._files())


def _read_groups(extracted_rows: typing.Iterable[typing.Dict[str, typing.Any]]
                ) -> typing.Iterator[typing.List[typing.Dict[str, typing.Any]]]:
    for group in itertools.groupby(extracted_rows, lambda y: y.get(dwelling.Dwelling.GROUPING_FIELD)):
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


def transform(extract_reader: ExtractProtocol, show_progress: bool = False) -> typing.Iterator[dwelling.Dwelling]:
    extracted_rows = tqdm(extract_reader.extracted_rows(), total=extract_reader.num_rows(),
                          unit=' files', disable=not show_progress)
    for row_group in _read_groups(extracted_rows):
        output = _generate_dwellings(row_group)
        if output:
            yield output
