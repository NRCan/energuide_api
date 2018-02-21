from io import BytesIO
import base64
import pytest
from azure.storage import blob
import azure_utils
import crypt_utils
import extract_endpoint

extract_endpoint.App.testing = True


@pytest.fixture
def sample_secret_key() -> str:
    extract_endpoint.App.config['SECRET_KEY'] = 'sample secret key'
    return extract_endpoint.App.config['SECRET_KEY']


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
def sample_storage_coordinates() -> azure_utils.StorageCoordinates:
    coords = azure_utils.StorageCoordinates(account='devstoreaccount1',
                                            key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uS'
                                            + 'RZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
                                            container='test-container',
                                            domain='http://127.0.0.1:10000/devstoreaccount1')
    extract_endpoint.App.config['AZURE_COORDINATES'] = coords
    return coords


@pytest.fixture
def sample_block_blob_service(sample_storage_coordinates: azure_utils.StorageCoordinates) -> blob.BlockBlobService:
    block_blob_service = blob.BlockBlobService(account_name=sample_storage_coordinates.account,
                                               account_key=sample_storage_coordinates.key,
                                               custom_domain=sample_storage_coordinates.domain)
    block_blob_service.create_container(sample_storage_coordinates.container)
    yield block_blob_service
    block_blob_service.delete_container(sample_storage_coordinates.container)


def test_test_alive() -> None:
    app = extract_endpoint.App.test_client()
    actual = app.get('/test_alive')
    assert b'Alive' in actual.data


def test_upload(sample_salt: str, sample_secret_key: str, sample_block_blob_service: blob.BlockBlobService,
                sample_storage_coordinates: azure_utils.StorageCoordinates, sample_file_contents: str,
                sample_file_name: str) -> None:
    app = extract_endpoint.App.test_client()
    file = BytesIO(sample_file_contents.encode('utf-8'))
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    file.seek(0)
    container = sample_storage_coordinates.container
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key, data=file_as_string)

    app.post('/upload_file', data=dict(salt=sample_salt, signature=signature, file=(file, sample_file_name)))

    assert sample_file_name in [blob.name for blob in sample_block_blob_service.list_blobs(container)]
    actual_blob = sample_block_blob_service.get_blob_to_text(container, sample_file_name)
    # sample_block_blob_service.delete_blob(container, sample_file_name)
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
