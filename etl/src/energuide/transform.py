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
            for file in sorted(zip_input.namelist()):
                content = zip_input.read(file)
                house = json.loads(content)
                house['jsonFileName'] = file
                yield house

    def num_rows(self) -> int:
        with zipfile.ZipFile(self._zip_filename) as zip_input:
            return len(zip_input.namelist())


class AzureExtractReader:
    tl_start_filename = 'timestamp_tl_start.txt'

    def __init__(self, coords: AzureCoordinates) -> None:
        self._coords = coords
        self._azure: typing.Optional[blob.BlockBlobService] = None
        self._new_file_list: typing.Optional[typing.List[str]] = None

    @property
    def _azure_service(self) -> blob.BlockBlobService:
        if self._azure is None:
            self._azure = blob.BlockBlobService(account_name=self._coords.account,
                                                account_key=self._coords.key,
                                                custom_domain=self._coords.domain)
        return self._azure

    @property
    def _new_files(self) -> typing.List[str]:
        if self._new_file_list is None:
            if self._azure_service.exists(self._coords.container, self.tl_start_filename):
                etl_start_properties = self._azure_service.get_blob_properties(self._coords.container,
                                                                               self.tl_start_filename)
                last_etl_start = etl_start_properties.properties.last_modified

                self._azure_service.create_blob_from_text(self._coords.container, self.tl_start_filename, 'TL start')

                new_blobs = [blob_ for blob_ in self._azure_service.list_blobs(self._coords.container)
                             if 'timestamp' not in blob_.name and blob_.properties.last_modified >= last_etl_start]
                new_eval_ids = set(blob_.name.split('-')[0] for blob_ in new_blobs if '-' in blob_.name)

                self._new_file_list = sorted([blob_.name
                                              for blob_ in self._azure_service.list_blobs(self._coords.container)
                                              if '-' in blob_.name and blob_.name.split('-')[0] in new_eval_ids])
            else:
                self._azure_service.create_blob_from_text(self._coords.container, self.tl_start_filename, 'TL start')
                self._new_file_list = sorted([blob_.name
                                              for blob_ in self._azure_service.list_blobs(self._coords.container)
                                              if 'timestamp' not in blob_.name])
        return self._new_file_list

    def extracted_rows(self) -> typing.Iterator[typing.Dict[str, typing.Any]]:
        for file in self._new_files:
            content = self._azure_service.get_blob_to_bytes(self._coords.container, file).content
            house = json.loads(content)
            house['jsonFileName'] = file
            yield house

    def num_rows(self) -> int:
        return len(self._new_files)


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
        full_message = logger.unwrap_exception_message(exc)

        LOGGER.error(
            f'Files: "{", ".join(files)}": {failing_type.__name__}'
            f' - {full_message}' if full_message else ''
        )
    except EnerguideError as exc:
        files = [str(file.get('jsonFileName')) for file in grouped]
        full_message = logger.unwrap_exception_message(exc)

        LOGGER.error(
            f'Files: "{", ".join(files)}"'
            f': {full_message}' if full_message else ''
        )
    return None


def transform(extract_reader: ExtractProtocol, show_progress: bool = False) -> typing.Iterator[dwelling.Dwelling]:
    extracted_rows = tqdm(extract_reader.extracted_rows(), total=extract_reader.num_rows(),
                          unit=' files', disable=not show_progress)
    for row_group in _read_groups(extracted_rows):
        output = _generate_dwellings(row_group)
        if output:
            yield output
