import os
from io import BytesIO
import typing
import pytest
from azure.storage.blob import BlockBlobService
from azure_utils import StorageCoordinates, upload_stream_to_azure, EnvVariables, DefaultVariables


@pytest.fixture
def sample_account() -> str:
    return os.environ.get(EnvVariables.account.value, DefaultVariables.account.value)


@pytest.fixture
def sample_key() -> str:
    return os.environ.get(EnvVariables.key.value, DefaultVariables.key.value)


@pytest.fixture
def sample_container() -> str:
    return os.environ.get(EnvVariables.container.value, DefaultVariables.container.value)


@pytest.fixture
def sample_domain() -> typing.Optional[str]:
    return os.environ.get(EnvVariables.domain.value, DefaultVariables.domain.value)


@pytest.fixture
def sample_storage_coordinates(sample_account: str,
                               sample_key: str,
                               sample_container: str,
                               sample_domain: typing.Optional[str]) -> StorageCoordinates:
    return StorageCoordinates(account=sample_account, key=sample_key,
                              container=sample_container, domain=sample_domain)


@pytest.fixture
def sample_block_blob_service(sample_storage_coordinates: StorageCoordinates) -> BlockBlobService:
    account, key, _, domain = sample_storage_coordinates
    return BlockBlobService(account_name=account, account_key=key, custom_domain=domain)


@pytest.fixture
def sample_stream_content()->str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content) -> BytesIO:
    return BytesIO(sample_stream_content.encode())


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


def test_upload_stream_to_azure(sample_storage_coordinates: StorageCoordinates,
                                sample_block_blob_service: BlockBlobService,
                                sample_container: str,
                                sample_stream: BytesIO,
                                sample_stream_content: str,
                                sample_filename: str) -> None:
    actual = upload_stream_to_azure(sample_storage_coordinates, sample_stream, sample_filename)
    assert 'succeeded' in actual.lower()
    assert sample_filename in [blob.name for blob in sample_block_blob_service.list_blobs(sample_container)]
    actual = sample_block_blob_service.get_blob_to_text(sample_container, sample_filename)
    sample_block_blob_service.delete_blob(sample_container, sample_filename)
    assert actual == sample_stream_content
