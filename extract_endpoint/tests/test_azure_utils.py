import io
import pytest
from azure.storage import blob
from extract_endpoint import azure_utils


@pytest.fixture
def sample_storage_coordinates() -> azure_utils.StorageCoordinates:
    return azure_utils.StorageCoordinates(account=azure_utils.AZURE_EMULATOR_ACCOUNT,
                                          key=azure_utils.AZURE_EMULATOR_KEY,
                                          container=azure_utils.AZURE_EMULATOR_CONTAINER,
                                          domain=azure_utils.AZURE_EMULATOR_DOMAIN)


@pytest.fixture
def sample_block_blob_service(sample_storage_coordinates: azure_utils.StorageCoordinates) -> blob.BlockBlobService:
    block_blob_service = blob.BlockBlobService(account_name=sample_storage_coordinates.account,
                                               account_key=sample_storage_coordinates.key,
                                               custom_domain=sample_storage_coordinates.domain)
    block_blob_service.create_container(sample_storage_coordinates.container)
    yield block_blob_service
    block_blob_service.delete_container(sample_storage_coordinates.container)


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
