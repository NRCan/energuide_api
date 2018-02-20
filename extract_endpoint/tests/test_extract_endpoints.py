import os
from io import BytesIO
import base64
import pytest
from azure.storage.blob import BlockBlobService
import azure_utils
import crypt_utils
import extract_endpoint

extract_endpoint.App.testing = True


@pytest.fixture
def sample_secret_key() -> str:
    return 'sample secret key'


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_file_contents() -> str:
    return 'sample file contents'


@pytest.fixture
def sample_file_name() -> str:
    return 'test_sample_blob_filename.txt'


@pytest.fixture
def sample_azure_account() -> str:
    return os.environ.get(azure_utils.EnvVariables.account.value, azure_utils.DefaultVariables.account.value)


@pytest.fixture
def sample_azure_key() -> str:
    return os.environ.get(azure_utils.EnvVariables.key.value, azure_utils.DefaultVariables.key.value)


@pytest.fixture
def sample_azure_container() -> str:
    return os.environ.get(azure_utils.EnvVariables.container.value, azure_utils.DefaultVariables.container.value)


@pytest.fixture
def sample_azure_domain() -> str:
    return os.environ.get(azure_utils.EnvVariables.domain.value, azure_utils.DefaultVariables.domain.value)


# @pytest.fixture
# def sample_storage_coordinates(sample_azure_account: str, sample_azure_key: str,
#                            sample_azure_container: str, sample_azure_domain: str) -> azure_utils.StorageCoordinates:
#     return azure_utils.StorageCoordinates(account=sample_azure_account, key=sample_azure_key,
#                                           container=sample_azure_container, domain=sample_azure_domain)


@pytest.fixture
# def sample_block_blob_service(sample_storage_coordinates: azure_utils.StorageCoordinates) -> BlockBlobService:
def sample_block_blob_service(sample_azure_account: str, sample_azure_key: str,
                              sample_azure_domain: str) -> BlockBlobService:

        # account, key, _, domain = sample_storage_coordinates
    # return BlockBlobService(account_name=account, account_key=key, custom_domain=domain)
    return BlockBlobService(account_name=sample_azure_account, account_key=sample_azure_key,
                            custom_domain=sample_azure_domain)


def test_test_alive() -> None:
    app = extract_endpoint.App.test_client()
    actual = app.get('/test_alive')
    assert b'Alive' in actual.data


def test_upload(sample_salt: str, sample_secret_key: str, sample_block_blob_service: BlockBlobService,
                sample_azure_container: str, sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    file.seek(0)
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)
    if sample_file_name in [blob.name for blob in sample_block_blob_service.list_blobs(sample_azure_container)]:
        sample_block_blob_service.delete_blob(sample_azure_container, sample_file_name)
    assert sample_file_name not in [blob.name for blob in sample_block_blob_service.list_blobs(sample_azure_container)]

    app.post('/upload_file', data=dict(salt=sample_salt, signature=signature, file=(file, sample_file_name)))

    assert sample_file_name in [blob.name for blob in sample_block_blob_service.list_blobs(sample_azure_container)]
    actual_blob = sample_block_blob_service.get_blob_to_text(sample_azure_container, sample_file_name)
    sample_block_blob_service.delete_blob(sample_azure_container, sample_file_name)
    assert actual_blob.content == sample_file_contents


def test_upload_no_key_in_env(sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = extract_endpoint.DEFAULT_ENDPOINT_SECRET_KEY
    app = extract_endpoint.App.test_client()
    stream = BytesIO(sample_file_contents.encode('utf-8'))
    with pytest.raises(ValueError):
        app.post('/upload_file', data=dict(file=(stream, sample_file_name)))


def test_upload_no_salt(sample_salt: str, sample_secret_key: str,
                        sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    file.seek(0)
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)
    actual = app.post('/upload_file', data=dict(signature=signature, file=(file, sample_file_name)))
    assert actual.status_code == 404


def test_upload_wrong_salt(sample_salt: str, sample_secret_key: str,
                           sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    file.seek(0)
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)
    actual = app.post('/upload_file', data=dict(salt='wrong salt', signature=signature, file=(file, sample_file_name)))
    assert actual.status_code == 404


def test_upload_no_signature(sample_salt: str, sample_secret_key: str,
                             sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(salt=sample_salt, file=(file, sample_file_name)))
    assert actual.status_code == 404


def test_upload_wrong_signature(sample_salt: str, sample_secret_key: str,
                                sample_file_contents: str, sample_file_name: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(salt=sample_salt, signature='wrong signature',
                                                file=(file, sample_file_name)))
    assert actual.status_code == 404


def test_upload_no_file(sample_salt: str, sample_secret_key: str, sample_file_contents: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)
    actual = app.post('/upload_file', data=dict(salt=sample_salt, signature=signature))
    assert actual.status_code == 404


def test_upload_no_filename(sample_salt: str, sample_secret_key: str, sample_file_contents: str) -> None:
    extract_endpoint.App.config['SECRET_KEY'] = sample_secret_key
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    file.seek(0)
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)
    actual = app.post('/upload_file', data=dict(salt=sample_salt, signature=signature, file=(file, '')))
    assert actual.status_code == 404
