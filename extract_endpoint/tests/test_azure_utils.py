import io
import pytest
from azure.storage import blob
import azure_utils


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
def sample_domain() -> str:
    return 'http://127.0.0.1:10000/devstoreaccount1'


@pytest.fixture
def sample_storage_coordinates(sample_account: str,
                               sample_key: str,
                               sample_container: str,
                               sample_domain: str) -> azure_utils.StorageCoordinates:
    return azure_utils.StorageCoordinates(account=sample_account, key=sample_key,
                                          container=sample_container, domain=sample_domain)


@pytest.fixture
def sample_block_blob_service(sample_storage_coordinates: azure_utils.StorageCoordinates) -> blob.BlockBlobService:
    block_blob_service = blob.BlockBlobService(account_name=sample_storage_coordinates.account,
                                               account_key=sample_storage_coordinates.key,
                                               custom_domain=sample_storage_coordinates.domain)
    container = sample_storage_coordinates.container
    for filename in [blob.name for blob in block_blob_service.list_blobs(container)]:
        block_blob_service.delete_blob(container, filename)
    return block_blob_service

@pytest.fixture
def sample_stream_content() -> str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content: str) -> io.BytesIO:
    return io.BytesIO(sample_stream_content.encode())


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


def test_upload_stream_to_azure(sample_storage_coordinates: azure_utils.StorageCoordinates,
                                sample_block_blob_service: blob.BlockBlobService,
                                sample_stream: io.BytesIO,
                                sample_stream_content: str,
                                sample_filename: str) -> None:
    assert azure_utils.upload_stream_to_azure(sample_storage_coordinates, sample_stream, sample_filename)
    container = sample_storage_coordinates.container
    assert sample_filename in [blob.name for blob in sample_block_blob_service.list_blobs(container)]
    actual_file_blob = sample_block_blob_service.get_blob_to_text(container, sample_filename)
    assert actual_file_blob.content == sample_stream_content
