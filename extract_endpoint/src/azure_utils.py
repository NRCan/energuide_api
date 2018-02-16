import enum
from io import BytesIO
import typing
from azure.storage.blob import BlockBlobService


class StorageCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


class EnvVariables(enum.Enum):
    account = 'AZURE_STORAGE_ACCOUNT'
    key = 'AZURE_STORAGE_KEY'
    container = 'AZURE_CONTAINER'
    domain = 'AZURE_STORAGE_DOMAIN'


class DefaultVariables(enum.Enum):
    account = 'account'
    key = 'key'
    container = 'container'
    domain = None


def upload_stream_to_azure(coords: StorageCoordinates, stream: BytesIO, filename: str) -> str:
    account, key, container, domain = coords
    azure_path = filename

    block_blob_service = BlockBlobService(account_name=account, account_key=key, custom_domain=domain)
    block_blob_service.create_blob_from_stream(container, azure_path, stream)

    if azure_path not in [blob.name for blob in block_blob_service.list_blobs(container)]:
        return "upload failed"
    return "upload succeeded"
