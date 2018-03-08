import enum
import typing
import typing_extensions
from azure.storage import blob


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


class LocalStorage:
    def __init__(self):
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
            self.upload_run_count += 1
            return True
        else:
            return False

    def download(self, filename: str) -> str:
        if filename:
            self.download_run_count += 1
            return filename
        else:
            return None


class AzureStorage:
    def __init__(self, coords: StorageCoordinates):
        self._coords = coords
        self._azure: typing.Optional[blob.BlockBlobService] = None

    @property
    def _azure_service(self) -> blob.BlockBlobService:
        if self._azure is None:
            self._azure = blob.BlockBlobService(account_name=self._coords.account,
                                                account_key=self._coords.key,
                                                custom_domain=self._coords.domain)
        return self._azure

    def upload(self, data: bytes, filename: str) -> bool:
        self._azure_service.create_blob_from_bytes(self._coords.container, filename, data)
        return filename in [blob.name for blob in self._azure.list_blobs(self._coords.container)]

    def download(self, filename: str) -> str:
        return self._azure_service.get_blob_to_bytes(self._coords.container, filename).content


def upload_bytes_to_azure(storage: StorageProtocol, data: bytes, filename: str) -> bool:
    result = storage.upload(data, filename)
    return result


def download_bytes_from_azure(storage: StorageProtocol, filename: str) -> str:
    result = storage.download(filename)
    return result


