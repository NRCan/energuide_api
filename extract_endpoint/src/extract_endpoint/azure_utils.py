import enum
import typing
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


def upload_bytes_to_azure(coords: StorageCoordinates, data: bytes, filename: str) -> bool:
    azure_service = blob.BlockBlobService(account_name=coords.account,
                                          account_key=coords.key,
                                          custom_domain=coords.domain)
    azure_service.create_blob_from_bytes(coords.container, filename, data)
    return filename in [blob.name for blob in azure_service.list_blobs(coords.container)]


def download_string_from_azure(coords: StorageCoordinates, filename: str) -> str:
    azure_service = blob.BlockBlobService(account_name=coords.account,
                                          account_key=coords.key,
                                          custom_domain=coords.domain)
    return azure_service.get_blob_to_text(coords.container, filename).content
