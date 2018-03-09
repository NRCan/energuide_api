import enum
import typing
from azure.storage import blob
import typing_extensions


class StorageCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


class EnvVariables(enum.Enum):
    account = 'EXTRACT_ENDPOINT_STORAGE_ACCOUNT'
    key = 'EXTRACT_ENDPOINT_STORAGE_KEY'
    container = 'EXTRACT_ENDPOINT_CONTAINER'
    domain = 'EXTRACT_ENDPOINT_STORAGE_DOMAIN'


class StorageProtocol(typing_extensions.Protocol):
    def upload(self, data: bytes, filename: str) -> bool:
        pass

    def download(self, filename: str) -> str:
        pass


class MockStorage:
    def __init__(self) -> None:
        self._upload_run_count = 0
        self._download_run_count = 0

    @property
    def upload_run_count(self) -> int:
        return self._upload_run_count

    @property
    def download_run_count(self) -> int:
        return self._download_run_count

    def upload(self, data: bytes, filename: str) -> bool:
        if data and filename:
            self._upload_run_count += 1
            return True
        return False

    def download(self, filename: str) -> str:
        if filename:
            self._download_run_count += 1
            return filename
        return 'bad_file_name'


class AzureStorage:
    def __init__(self, coords: StorageCoordinates) -> None:
        self._coords = coords
        self._azure_service = blob.BlockBlobService(account_name=self._coords.account,
                                                    account_key=self._coords.key,
                                                    custom_domain=self._coords.domain)

    def upload(self, data: bytes, filename: str) -> bool:
        self._azure_service.create_blob_from_bytes(self._coords.container, filename, data)
        return filename in [blob.name for blob in self._azure_service.list_blobs(self._coords.container)]

    def download(self, filename: str) -> str:
        return self._azure_service.get_blob_to_bytes(self._coords.container, filename).content


def upload_bytes_to_azure(storage: StorageProtocol, data: bytes, filename: str) -> bool:
    result = storage.upload(data, filename)
    return result


def download_bytes_from_azure(storage: StorageProtocol, filename: str) -> str:
    result = storage.download(filename)
    return result
