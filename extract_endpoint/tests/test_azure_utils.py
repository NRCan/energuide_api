import pytest
from azure.storage import blob
from extract_endpoint import azure_utils


@pytest.fixture
def sample_stream_content() -> str:
    return "Sample stream content"


@pytest.fixture
def sample_data(sample_stream_content: str) -> bytes:
    return sample_stream_content.encode()


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


def test_upload_bytes_to_azure(azure_emulator_coords: azure_utils.StorageCoordinates,
                               azure_service: blob.BlockBlobService,
                               sample_data: bytes,
                               sample_stream_content: str,
                               sample_filename: str) -> None:

    assert azure_utils.upload_bytes_to_azure(azure_emulator_coords, sample_data, sample_filename)
    assert sample_filename in \
           [blob.name for blob in azure_service.list_blobs(azure_emulator_coords.container)]
    actual_file_blob = azure_service.get_blob_to_text(azure_emulator_coords.container, sample_filename)
    assert actual_file_blob.content == sample_stream_content
