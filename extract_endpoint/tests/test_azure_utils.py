import typing
import pytest
from azure.storage import blob
from azure.common import AzureMissingResourceHttpError
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


@pytest.fixture
def put_file_in_azure(azure_emulator_coords: azure_utils.StorageCoordinates,
                      azure_service: blob.BlockBlobService,
                      sample_stream_content: str) -> typing.Generator:

    filename = 'test_put_file.txt'
    azure_service.create_blob_from_text(azure_emulator_coords.container, filename, sample_stream_content)
    yield filename
    azure_service.delete_blob(azure_emulator_coords.container, filename)


def check_file_in_azure(azure_service: blob.BlockBlobService,
                        azure_emulator_coords: azure_utils.StorageCoordinates,
                        filename: str,
                        contents: str) -> None:

    assert filename in [blob.name for blob in azure_service.list_blobs(azure_emulator_coords.container)]
    actual_blob = azure_service.get_blob_to_text(azure_emulator_coords.container, filename)
    assert actual_blob.content == contents


def test_upload_bytes(azure_emulator_coords: azure_utils.StorageCoordinates,
                      azure_service: blob.BlockBlobService,
                      sample_data: bytes,
                      sample_stream_content: str,
                      sample_filename: str) -> None:

    assert azure_utils.upload_bytes_to_azure(azure_emulator_coords, sample_data, sample_filename)
    check_file_in_azure(azure_service, azure_emulator_coords, sample_filename, sample_stream_content)


def test_download_bytes(azure_emulator_coords: azure_utils.StorageCoordinates,
                        put_file_in_azure: str,
                        sample_stream_content: str) -> None:

    actual_contents = azure_utils.download_bytes_from_azure(azure_emulator_coords, put_file_in_azure)
    assert actual_contents == sample_stream_content.encode()


@pytest.mark.usefixtures('put_file_in_azure')
def test_download_bytes_bad_filename(azure_emulator_coords: azure_utils.StorageCoordinates) -> None:
    with pytest.raises(AzureMissingResourceHttpError):
        azure_utils.download_bytes_from_azure(azure_emulator_coords, 'bad_filename')
