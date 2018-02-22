import io
import base64
import pytest
from flask import testing
from azure.storage import blob
import azure_utils
import crypt_utils
import extract_endpoint


extract_endpoint.App.testing = True


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
    return blob.BlockBlobService(account_name=sample_storage_coordinates.account,
                                 account_key=sample_storage_coordinates.key,
                                 custom_domain=sample_storage_coordinates.domain)


@pytest.fixture
def test_client(sample_block_blob_service, sample_storage_coordinates) -> testing.FlaskClient:
    sample_block_blob_service.create_container(sample_storage_coordinates.container)
    yield extract_endpoint.App.test_client()
    sample_block_blob_service.delete_container(sample_storage_coordinates.container)


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_secret_key() -> str:
    extract_endpoint.App.config['SECRET_KEY'] = 'sample secret key'
    return extract_endpoint.App.config['SECRET_KEY']


@pytest.fixture
def sample_stream_content() -> str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content: str) -> io.BytesIO:
    return io.BytesIO(sample_stream_content.encode())


@pytest.fixture
def sample_signature(sample_salt: str, sample_secret_key: str, sample_stream: io.BytesIO) -> str:
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key,
                                        data=base64.b64encode(sample_stream.read()).decode('utf-8'))
    sample_stream.seek(0)
    return signature


@pytest.fixture
def sample_file_name() -> str:
    return 'test_sample_blob_filename.txt'


def test_test_alive(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/test_alive')
    assert b'Alive' in get_return.data


def test_robots(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/robots933456.txt')
    assert get_return.status_code == 404


def test_upload(test_client: testing.FlaskClient,
                sample_storage_coordinates: azure_utils.StorageCoordinates,
                sample_block_blob_service: blob.BlockBlobService,
                sample_salt: str,
                sample_signature: str,
                sample_stream_content: str,
                sample_stream: io.BytesIO,
                sample_file_name: str) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_signature,
                                                             filename=sample_file_name,
                                                             file=(sample_stream, sample_file_name)))
    assert post_return.status_code == 200
    assert sample_file_name in [blob.name for blob in
                                sample_block_blob_service.list_blobs(sample_storage_coordinates.container)]
    actual_blob = sample_block_blob_service.get_blob_to_text(sample_storage_coordinates.container, sample_file_name)
    assert actual_blob.content == sample_stream_content


def test_upload_no_key_in_env(test_client: testing.FlaskClient,
                              sample_salt: str, sample_signature: str,
                              sample_stream: io.BytesIO,
                              sample_file_name: str) -> None:

    extract_endpoint.App.config['SECRET_KEY'] = extract_endpoint.DEFAULT_ENDPOINT_SECRET_KEY
    with pytest.raises(ValueError):
        test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_signature,
                                                   filename=sample_file_name, file=(sample_stream, sample_file_name)))


def test_upload_no_salt(test_client: testing.FlaskClient,
                        sample_signature: str,
                        sample_stream: io.BytesIO,
                        sample_file_name: str) -> None:
    post_return = test_client.post('/upload_file', data=dict(signature=sample_signature, filename=sample_file_name,
                                                             file=(sample_stream, sample_file_name)))
    assert post_return.status_code == 404


def test_upload_wrong_salt(test_client: testing.FlaskClient,
                           sample_signature: str,
                           sample_stream: io.BytesIO,
                           sample_file_name: str) -> None:
    post_return = test_client.post('/upload_file', data=dict(salt='wrong salt', signature=sample_signature,
                                                             filename=sample_file_name,
                                                             file=(sample_stream, sample_file_name)))
    assert post_return.status_code == 404


def test_upload_no_signature(test_client: testing.FlaskClient,
                             sample_salt: str,
                             sample_stream: io.BytesIO,
                             sample_file_name: str) -> None:
    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, filename=sample_file_name,
                                                             file=(sample_stream, sample_file_name)))
    assert post_return.status_code == 404


def test_upload_wrong_signature(test_client: testing.FlaskClient,
                                sample_salt: str,
                                sample_stream: io.BytesIO,
                                sample_file_name: str) -> None:
    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature='wrong signature',
                                                             filename=sample_file_name,
                                                             file=(sample_stream, sample_file_name)))
    assert post_return.status_code == 404


def test_upload_no_file(test_client: testing.FlaskClient,
                        sample_salt: str, sample_signature: str) -> None:
    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_signature,
                                                             filename=sample_file_name))
    assert post_return.status_code == 404


def test_upload_no_filename(test_client: testing.FlaskClient,
                            sample_salt: str,
                            sample_signature: str,
                            sample_stream: io.BytesIO) -> None:
    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_signature,
                                                             filename=sample_file_name, file=(sample_stream, '')))
    assert post_return.status_code == 404
