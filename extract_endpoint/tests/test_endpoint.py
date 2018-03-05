import io
import base64
import hashlib
import requests
from http import HTTPStatus
import typing
import pytest
from flask import testing
from azure.storage import blob
from extract_endpoint import azure_utils
from extract_endpoint import crypt_utils
from extract_endpoint import endpoint


endpoint.App.testing = True


@pytest.fixture
def test_client(monkeypatch, azure_emulator_coords: azure_utils.StorageCoordinates) -> testing.FlaskClient:
    monkeypatch.setitem(endpoint.App.config, 'AZURE_COORDINATES', azure_emulator_coords)
    return endpoint.App.test_client()


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_secret_key(monkeypatch) -> str:
    monkeypatch.setitem(endpoint.App.config, 'SECRET_KEY', 'sample secret key')
    return endpoint.App.config['SECRET_KEY']


@pytest.fixture
def sample_salt_signature(sample_salt: str, sample_secret_key: str) -> str:
    hasher = hashlib.new('sha3_256')
    hasher.update((sample_salt + sample_secret_key).encode())
    return hasher.hexdigest()


@pytest.fixture
def sample_zipfile_signature(sample_salt: str, sample_secret_key: str, sample_zipfile: io.BytesIO) -> str:
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key,
                                        data=base64.b64encode(sample_zipfile.read()).decode('utf-8'))
    sample_zipfile.seek(0)
    return signature


@pytest.fixture
def sample_nonzipfile() -> io.BytesIO:
    return io.BytesIO(b'Not a zipfile')


@pytest.fixture
def sample_nonzipfile_signature(sample_salt: str, sample_secret_key: str, sample_nonzipfile: io.BytesIO) -> str:
    signature = crypt_utils.sign_string(salt=sample_salt, key=sample_secret_key,
                                        data=base64.b64encode(sample_nonzipfile.read()).decode('utf-8'))
    sample_nonzipfile.seek(0)
    return signature


@pytest.fixture
def upload_timestamp_file(azure_emulator_coords: azure_utils.StorageCoordinates,
                          azure_service: blob.BlockBlobService,
                          sample_timestamp: str) -> typing.Generator:

    azure_service.create_blob_from_text(azure_emulator_coords.container, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    yield
    azure_service.delete_blob(azure_emulator_coords.container, endpoint.TIMESTAMP_FILENAME)


@pytest.fixture
def sample_trigger_tl_url(monkeypatch) -> str:
    url = 'http:trigger.url/trigger_tl'
    monkeypatch.setenv('TRIGGER_URL', url)
    return url


@pytest.fixture
def mocked_tl_app(monkeypatch, sample_secret_key: str, sample_trigger_tl_url: str):
    def mocked_post(url: str, data: typing.Dict[str, str]):
        mock = type('MockedReq', (), {})()

        if url != sample_trigger_tl_url:
            mock.status_code = HTTPStatus.NOT_FOUND
            mock.content = 'not trigger url'

        if 'salt' not in data or 'signature' not in data:
            mock.status_code = HTTPStatus.BAD_REQUEST
            mock.content = 'missing salt or sig'
        else:
            salt = data['salt']
            signature = data['signature']
            hasher = hashlib.new('sha3_256')
            hasher.update((salt + sample_secret_key).encode())
            expected_signature = hasher.hexdigest()

            if expected_signature == signature:
                mock.status_code = HTTPStatus.CREATED
                mock.content = 'success'
            else:
                mock.content = 'failed'
                mock.status_code = HTTPStatus.BAD_REQUEST
        return mock

    monkeypatch.setattr(requests, 'post', mocked_post)


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger(sample_salt: str, sample_salt_signature: str) -> None:
    return_val = endpoint.trigger('http://url', sample_salt, sample_salt_signature)
    assert return_val[1] == HTTPStatus.CREATED


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger_no_salt() -> None:
    return_val = endpoint.trigger('http://url')
    assert return_val[1] == HTTPStatus.CREATED


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger_tl(test_client: testing.FlaskClient, sample_salt: str, sample_salt_signature: str) -> None:

    return_val = test_client.post('/trigger_tl', data=dict(salt=sample_salt, signature=sample_salt_signature))
    assert return_val.status_code == HTTPStatus.CREATED


def test_frontend(test_client: testing.FlaskClient) -> None:
    assert test_client.get('/').status_code == HTTPStatus.OK


def test_alive(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/test_alive')
    assert b'Alive' in get_return.data


def test_robots(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/robots933456.txt')
    assert get_return.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.usefixtures('upload_timestamp_file')
def test_timestamp(test_client: testing.FlaskClient, sample_timestamp: str) -> None:
    get_return = test_client.get('/timestamp')
    assert get_return.data == sample_timestamp.encode()


def test_timestamp_no_file(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/timestamp')
    assert get_return.status_code == HTTPStatus.BAD_GATEWAY


def check_file_in_azure(azure_service: blob.BlockBlobService,
                        azure_emulator_coords: azure_utils.StorageCoordinates,
                        filename: str,
                        contents: str) -> None:

    assert filename in [blob.name for blob in azure_service.list_blobs(azure_emulator_coords.container)]
    actual_blob = azure_service.get_blob_to_text(azure_emulator_coords.container, filename)
    assert actual_blob.content == contents


@pytest.mark.usefixtures('mocked_tl_app')
def test_upload_with_timestamp(azure_emulator_coords: azure_utils.StorageCoordinates,
                               test_client: testing.FlaskClient,
                               azure_service: blob.BlockBlobService,
                               sample_timestamp: str,
                               sample_salt: str,
                               sample_zipfile_signature: str,
                               sample_file_contents: str,
                               sample_filenames: str,
                               sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.CREATED
    check_file_in_azure(azure_service, azure_emulator_coords, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    for name, contents in zip(sample_filenames, sample_file_contents):
        check_file_in_azure(azure_service, azure_emulator_coords, name, contents)


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_without_timestamp(test_client: testing.FlaskClient,
                                  sample_salt: str,
                                  sample_zipfile_signature: str,
                                  sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_no_key_in_env(test_client: testing.FlaskClient,
                              sample_timestamp: str,
                              sample_salt: str,
                              sample_zipfile_signature: str,
                              sample_zipfile: io.BytesIO) -> None:

    endpoint.App.config['SECRET_KEY'] = endpoint.DEFAULT_ENDPOINT_SECRET_KEY
    with pytest.raises(ValueError):
        test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                   timestamp=sample_timestamp, file=(sample_zipfile, 'zipfile')))


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_no_salt(test_client: testing.FlaskClient,
                        sample_timestamp: str,
                        sample_zipfile_signature: str,
                        sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_wrong_salt(test_client: testing.FlaskClient,
                           sample_timestamp: str,
                           sample_zipfile_signature: str,
                           sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt='wrong salt', signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'sample_secret_key', 'mocked_tl_app')
def test_upload_no_signature(test_client: testing.FlaskClient,
                             sample_timestamp: str,
                             sample_salt: str,
                             sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'sample_secret_key', 'mocked_tl_app')
def test_upload_wrong_signature(test_client: testing.FlaskClient,
                                sample_timestamp: str,
                                sample_salt: str,
                                sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature='wrong signature',
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_no_file(test_client: testing.FlaskClient,
                        sample_timestamp: str,
                        sample_salt: str,
                        sample_zipfile_signature: str) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_with_non_zipfile(test_client: testing.FlaskClient,
                                 sample_timestamp: str,
                                 sample_salt: str,
                                 sample_nonzipfile_signature: str,
                                 sample_nonzipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_nonzipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_nonzipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b"Bad Zipfile" in post_return.data
