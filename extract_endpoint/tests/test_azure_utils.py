from io import BytesIO
from typing import Optional
import pytest
from azure.storage.blob import BlockBlobService
from azure_utils import StorageCoordinates, upload_stream_to_azure


@pytest.fixture
def sample_account() -> str:
    return 'devstoreaccount1'


@pytest.fixture
def sample_key() -> str:
    return 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='


@pytest.fixture
def sample_container() -> str:
    return 'energuide-extracted-data'


@pytest.fixture
def sample_domain() -> Optional[str]:
    return 'http://127.0.0.1:10000/devstoreaccount1'


@pytest.fixture
def sample_storage_coordinates(sample_account: str,
                               sample_key: str,
                               sample_container: str,
                               sample_domain: Optional[str]) -> StorageCoordinates:
    return StorageCoordinates(account=sample_account, key=sample_key, container=sample_container, domain=sample_domain)


@pytest.fixture
def sample_block_blob_service(sample_storage_coordinates: StorageCoordinates) -> BlockBlobService:
    account, key, _, domain = sample_storage_coordinates
    return BlockBlobService(account_name=account, account_key=key, custom_domain=domain)


@pytest.fixture
def sample_stream_content()->str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content: str) -> BytesIO:
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

    if isinstance(actual, str):
        assert actual == sample_stream_content
    else:
        assert actual.content == sample_stream_content
