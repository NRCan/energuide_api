import enum
from io import BytesIO
import os
import typing

from azure.storage.blob import BlockBlobService

class EnvVariables(enum.Enum):
    account = 'EXTRACTOR_STORAGE_ACCOUNT'
    key = 'EXTRACTOR_STORAGE_KEY'
    container = 'EXTRACTOR_CONTAINER'
    domain = 'EXTRACTOR_STORAGE_DOMAIN'


class EnvDefaults(enum.Enum):
    account = 'account'
    key = 'key'
    container = 'container'
    domain = None


class StorageCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


def upload_file_to_azure(coords: StorageCoordinates, data: str) -> str:
    account, key, container, domain = coords
    azure_path = os.path.basename(data.rstrip('/\\'))
    print(azure_path)

    block_blob_service = BlockBlobService(account_name=account, account_key=key, custom_domain=domain)
    block_blob_service.create_blob_from_path(container, azure_path, data)

    return azure_path


def upload_stream_to_azure(coords: StorageCoordinates, stream: BytesIO, filename: str) -> str:
    account, key, container, domain = coords
    azure_path = filename
    print(azure_path)

    block_blob_service = BlockBlobService(account_name=account, account_key=key, custom_domain=domain)
    block_blob_service.create_blob_from_stream(container, azure_path, stream)

    return azure_path