import enum
import typing
from azure.storage import blob


class StorageCoordinates(typing.NamedTuple):
    account: str
    key: str
    container: str
    domain: typing.Optional[str]


AZURE_EMULATOR_COORDS = StorageCoordinates(
    account='devstoreaccount1',
    key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
    container='test-container',
    domain='http://127.0.0.1:10000/devstoreaccount1',
)


class EnvVariables(enum.Enum):
    account = 'EXTRACT_ENDPOINT_STORAGE_ACCOUNT'
    key = 'EXTRACT_ENDPOINT_STORAGE_KEY'
    container = 'EXTRACT_ENDPOINT_CONTAINER'
    domain = 'EXTRACT_ENDPOINT_STORAGE_DOMAIN'


class DefaultVariables(enum.Enum):
    account = AZURE_EMULATOR_COORDS.account
    key = AZURE_EMULATOR_COORDS.key
    container = AZURE_EMULATOR_COORDS.container
    domain = None


def upload_stream_to_azure(coords: StorageCoordinates, stream: typing.IO[bytes], filename: str) -> bool:
    azure_service = blob.BlockBlobService(account_name=coords.account, account_key=coords.key,
                                          custom_domain=coords.domain)
    azure_service.create_blob_from_stream(coords.container, filename, stream)
    return filename in [blob.name for blob in azure_service.list_blobs(coords.container)]
