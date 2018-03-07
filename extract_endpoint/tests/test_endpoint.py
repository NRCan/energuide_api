import io
import hashlib
from http import HTTPStatus
import typing
import pytest
import _pytest
from flask import testing
from azure.storage import blob
from extract_endpoint import azure_utils
from extract_endpoint import endpoint


endpoint.App.testing = True


@pytest.fixture
def test_client(monkeypatch: _pytest.monkeypatch.MonkeyPatch,
                azure_emulator_coords: azure_utils.StorageCoordinates) -> testing.FlaskClient:

    monkeypatch.setitem(endpoint.App.config, 'AZURE_COORDINATES', azure_emulator_coords)
    return endpoint.App.test_client()


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_salt_signature(sample_salt: str, sample_secret_key: str) -> str:
    hasher = hashlib.new('sha3_256')
    hasher.update((sample_salt + sample_secret_key).encode())
    return hasher.hexdigest()


@pytest.fixture
def sample_zipfile_signature(sample_salt: str, sample_secret_key: str, sample_zipfile: io.BytesIO) -> str:
    hasher = hashlib.new('sha3_256')
    hasher.update((sample_salt + sample_secret_key).encode())
    hasher.update(sample_zipfile.read())
    sample_zipfile.seek(0)
    signature = hasher.hexdigest()
    return signature


@pytest.fixture
def sample_nonzipfile() -> io.BytesIO:
    return io.BytesIO(b'Not a zipfile')


@pytest.fixture
def sample_nonzipfile_signature(sample_salt: str, sample_secret_key: str, sample_nonzipfile: io.BytesIO) -> str:
    hasher = hashlib.new('sha3_256')
    hasher.update((sample_salt + sample_secret_key).encode())
    hasher.update(sample_nonzipfile.read())
    sample_nonzipfile.seek(0)
    signature = hasher.hexdigest()
    return signature


@pytest.fixture
def upload_timestamp_file(azure_emulator_coords: azure_utils.StorageCoordinates,
                          azure_service: blob.BlockBlobService,
                          sample_timestamp: str) -> typing.Generator:

    azure_service.create_blob_from_text(azure_emulator_coords.container, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    yield
    azure_service.delete_blob(azure_emulator_coords.container, endpoint.TIMESTAMP_FILENAME)


@pytest.fixture
def mocked_tl_app(monkeypatch, sample_secret_key: str):
    def mock_send_to_trigger(data: typing.Dict[str, str]) -> int:
        if 'salt' not in data:
            return HTTPStatus.BAD_REQUEST
        if 'signature' not in data:
            return HTTPStatus.BAD_REQUEST
        hasher = hashlib.new('sha3_256')
        hasher.update((data['salt'] + sample_secret_key).encode())
        actual_signature = hasher.hexdigest()
        if data['signature'] != actual_signature:
            return HTTPStatus.BAD_REQUEST
        return HTTPStatus.CREATED
    monkeypatch.setattr(endpoint, 'send_to_trigger', mock_send_to_trigger)


def test_trigger_url(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:
    monkeypatch.setenv('TRIGGER_ADDRESS', 'https://www.nrcan.ca:4000')
    assert endpoint._trigger_url() == 'https://www.nrcan.ca:4000/run_tl'


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger(sample_salt: str, sample_salt_signature: str) -> None:
    return_val = endpoint.trigger(dict(salt=sample_salt, signature=sample_salt_signature))
    assert return_val == HTTPStatus.CREATED


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger_no_data() -> None:
    return_val = endpoint.trigger()
    assert return_val == HTTPStatus.CREATED


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger_bad_data() -> None:
    return_val = endpoint.trigger(dict(salt='bad salt', signature='bad signature'))
    assert return_val == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('mocked_tl_app')
def test_trigger_route(test_client: testing.FlaskClient, sample_salt: str, sample_salt_signature: str) -> None:
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


@pytest.mark.usefixtures('azure_service', 'mocked_tl_app')
def test_upload_with_timestamp(test_client: testing.FlaskClient,
                               sample_timestamp: str,
                               sample_salt: str,
                               sample_zipfile_signature: str,
                               sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.CREATED


def test_upload_without_timestamp(test_client: testing.FlaskClient,
                                  sample_salt: str,
                                  sample_zipfile_signature: str,
                                  sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


def test_upload_no_key_in_env(test_client: testing.FlaskClient,
                              sample_timestamp: str,
                              sample_salt: str,
                              sample_zipfile_signature: str,
                              sample_zipfile: io.BytesIO) -> None:

    endpoint.App.config['SECRET_KEY'] = endpoint.DEFAULT_ETL_SECRET_KEY
    with pytest.raises(ValueError):
        test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                   timestamp=sample_timestamp, file=(sample_zipfile, 'zipfile')))


def test_upload_no_salt(test_client: testing.FlaskClient,
                        sample_timestamp: str,
                        sample_zipfile_signature: str,
                        sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


def test_upload_wrong_salt(test_client: testing.FlaskClient,
                           sample_timestamp: str,
                           sample_zipfile_signature: str,
                           sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt='wrong salt', signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('sample_secret_key')
def test_upload_no_signature(test_client: testing.FlaskClient,
                             sample_timestamp: str,
                             sample_salt: str,
                             sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('sample_secret_key')
def test_upload_wrong_signature(test_client: testing.FlaskClient,
                                sample_timestamp: str,
                                sample_salt: str,
                                sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature='wrong signature',
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


def test_upload_no_file(test_client: testing.FlaskClient,
                        sample_timestamp: str,
                        sample_salt: str,
                        sample_zipfile_signature: str) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST


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
