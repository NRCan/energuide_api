import os
from io import BytesIO
import pytest
from azure.storage.blob import BlockBlobService
from azure_storage import EnvVariables, EnvDefaults, StorageCoordinates
from extract_endpoint import extract_endpoint

extract_endpoint.App.testing = True


@pytest.fixture
def test_file_contents() -> str:
    return 'test_contents'


@pytest.fixture
def test_file_name() -> str:
    return 'test_blob_filename_989.txt'


@pytest.fixture
def account() -> str:
    return os.environ.get(EnvVariables.account.value, EnvDefaults.account.value)


@pytest.fixture
def key() -> str:
    return os.environ.get(EnvVariables.key.value, EnvDefaults.key.value)


@pytest.fixture
def container() -> str:
    return os.environ.get(EnvVariables.container.value, EnvDefaults.container.value)


@pytest.fixture
def domain() -> str:
    return os.environ.get(EnvVariables.domain.value, EnvDefaults.domain.value)


@pytest.fixture
def storage_coordinates(account: str, key: str, container: str, domain: str) -> StorageCoordinates:
    return StorageCoordinates(account=account, key=key, container=container, domain=domain)


@pytest.fixture
def block_blob_service(storage_coordinates: StorageCoordinates) -> BlockBlobService:
    account, key, _, domain = storage_coordinates
    return BlockBlobService(account_name=account, account_key=key, custom_domain=domain)


def test_frontend() -> None:
    app = extract_endpoint.App.test_client()
    actual = app.get('/frontend')
    assert b'Upload new File' in actual.data


def test_upload_no_key(test_file_contents: str, test_file_name: str) -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(test_file_contents.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(file=(stream, test_file_name)))
    assert actual.status_code == 404


def test_upload_wrong_key(test_file_contents: str, test_file_name: str) -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(test_file_contents.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(key='bad key', file=(stream, test_file_name)))
    assert actual.status_code == 404


def test_upload(block_blob_service: BlockBlobService, container: str,
                test_file_contents: str, test_file_name: str) -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(test_file_contents.encode('utf-8'))
    app.post('/upload_file', data=dict(key='development_key', file=(stream, test_file_name)))

    assert test_file_name in [blob.name for blob in block_blob_service.list_blobs(container)]
    actual = block_blob_service.get_blob_to_text(container, test_file_name)
    block_blob_service.delete_blob(container, test_file_name)
    assert actual.content == test_file_contents
