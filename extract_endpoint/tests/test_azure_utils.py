import typing
import pytest
from azure.storage import blob
from azure.common import AzureMissingResourceHttpError
from extract_endpoint import azure_utils


@pytest.fixture
def azure_storage(azure_emulator_coords: azure_utils.StorageCoordinates) -> azure_utils.AzureStorage:
    storage = azure_utils.AzureStorage(azure_emulator_coords)
    return storage


@pytest.fixture
def local_storage() -> azure_utils.LocalStorage:
    storage = azure_utils.LocalStorage()
    return storage


@pytest.fixture
def azure_test_service(azure_emulator_coords: azure_utils.StorageCoordinates) -> blob.BlockBlobService:
    azure_test_service = blob.BlockBlobService(account_name=azure_emulator_coords.account,
                                               account_key=azure_emulator_coords.key,
                                               custom_domain=azure_emulator_coords.domain)
    azure_test_service.create_container(azure_emulator_coords.container)
    yield azure_test_service
    azure_test_service.delete_container(azure_emulator_coords.container)


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
                      azure_test_service: blob.BlockBlobService,
                      sample_stream_content: str) -> typing.Generator:

    filename = 'test_put_file.txt'
    azure_test_service.create_blob_from_text(azure_emulator_coords.container, filename, sample_stream_content)
    yield filename
    azure_test_service.delete_blob(azure_emulator_coords.container, filename)


def check_file_in_azure(azure_test_service: blob.BlockBlobService,
                        azure_emulator_coords: azure_utils.StorageCoordinates,
                        filename: str,
                        contents: str) -> None:

    assert filename in [blob.name for blob in azure_test_service.list_blobs(azure_emulator_coords.container)]
    actual_blob = azure_test_service.get_blob_to_text(azure_emulator_coords.container, filename)
    assert actual_blob.content == contents


def test_upload_bytes(azure_storage: azure_utils.AzureStorage,
                      azure_test_service: blob.BlockBlobService,
                      sample_data: bytes,
                      sample_stream_content: str,
                      sample_filename: str,
                      azure_emulator_coords: azure_utils.StorageCoordinates,) -> None:

    assert azure_utils.upload_bytes_to_azure(azure_storage, sample_data, sample_filename)
    check_file_in_azure(azure_test_service, azure_emulator_coords, sample_filename, sample_stream_content)


def test_download_bytes(azure_storage: azure_utils.AzureStorage,
                        put_file_in_azure: str,
                        sample_stream_content: str) -> None:

    actual_contents = azure_utils.download_bytes_from_azure(azure_storage, put_file_in_azure)
    assert actual_contents == sample_stream_content.encode()


def test_local_storage_upload(local_storage: azure_utils.LocalStorage,
                              sample_data: bytes,
                              sample_filename: str) -> None:

    azure_utils.upload_bytes_to_azure(local_storage, sample_data, sample_filename)
    assert local_storage.upload_run_count == 1


def test_local_storage_download(local_storage: azure_utils.LocalStorage,
                                sample_filename: str) -> None:

    azure_utils.download_bytes_from_azure(local_storage, sample_filename)
    assert local_storage.download_run_count == 1



@pytest.mark.usefixtures('put_file_in_azure')
def test_download_bytes_bad_filename(azure_storage: azure_utils.AzureStorage) -> None:
    with pytest.raises(AzureMissingResourceHttpError):
        azure_utils.download_bytes_from_azure(azure_storage, 'bad_filename')
