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
def mocked_tl_app(monkeypatch: _pytest.monkeypatch.MonkeyPatch, sample_secret_key: str):
    def mock_send_to_tl(data: typing.Dict[str, str]) -> int:
        if 'salt' not in data:
            return HTTPStatus.BAD_REQUEST
        if 'signature' not in data:
            return HTTPStatus.BAD_REQUEST
        hasher = hashlib.new('sha3_256')
        hasher.update((data['salt'] + sample_secret_key).encode())
        actual_signature = hasher.hexdigest()
        if data['signature'] != actual_signature:
            return HTTPStatus.BAD_REQUEST
        return HTTPStatus.OK
    monkeypatch.setattr(endpoint, 'send_to_tl', mock_send_to_tl)


@pytest.fixture()
def thread_runner() -> typing.Generator:
    yield endpoint.ThreadRunner
    endpoint.ThreadRunner.join()


@pytest.fixture
def busy_thread_runner(thread_runner: endpoint.ThreadRunner) -> typing.Generator:
    stay_asleep = True

    def sleeper() -> None:
        while stay_asleep:
            pass

    thread_runner.start_new_thread(sleeper)
    yield thread_runner
    stay_asleep = False


def test_threadrunner(thread_runner: endpoint.ThreadRunner) -> None:
    stay_asleep = True

    def sleeper() -> None:
        while stay_asleep:
            pass

    thread_runner.start_new_thread(sleeper)
    assert thread_runner.is_thread_running()
    stay_asleep = False
    thread_runner.join()
    assert not thread_runner.is_thread_running()


def check_file_in_azure(azure_service: blob.BlockBlobService,
                        azure_emulator_coords: azure_utils.StorageCoordinates,
                        filename: str,
                        contents: str) -> None:

    assert filename in [blob.name for blob in azure_service.list_blobs(azure_emulator_coords.container)]
    actual_blob = azure_service.get_blob_to_text(azure_emulator_coords.container, filename)
    assert actual_blob.content == contents


def test_run_tl_url(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:
    monkeypatch.setenv('TL_ADDRESS', 'https://www.nrcan.ca:4000')
    assert endpoint._run_tl_url() == 'https://www.nrcan.ca:4000/run_tl'


@pytest.mark.usefixtures('mocked_tl_app')
def test_run_tl(sample_salt: str, sample_salt_signature: str) -> None:
    return_val = endpoint.run_tl(dict(salt=sample_salt, signature=sample_salt_signature))
    assert return_val == HTTPStatus.OK


@pytest.mark.usefixtures('mocked_tl_app')
def test_run_tl_no_data() -> None:
    return_val = endpoint.run_tl()
    assert return_val == HTTPStatus.OK


@pytest.mark.usefixtures('mocked_tl_app')
def test_run_tl_bad_data() -> None:
    return_val = endpoint.run_tl(dict(salt='bad salt', signature='bad signature'))
    assert return_val == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('mocked_tl_app')
def test_run_tl_route(test_client: testing.FlaskClient, sample_salt: str, sample_salt_signature: str) -> None:
    return_val = test_client.post('/run_tl', data=dict(salt=sample_salt, signature=sample_salt_signature))
    assert return_val.status_code == HTTPStatus.OK


@pytest.mark.usefixtures('mocked_tl_app', 'sample_secret_key')
def test_run_tl_route_no_data(test_client: testing.FlaskClient) -> None:
    return_val = test_client.post('/run_tl')
    assert return_val.status_code == HTTPStatus.BAD_REQUEST


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


def test_upload_with_timestamp(azure_service: blob.BlockBlobService,
                               azure_emulator_coords: azure_utils.StorageCoordinates,
                               sample_filenames: typing.Tuple[str, str],
                               sample_file_contents: typing.Tuple[str, str],
                               test_client: testing.FlaskClient,
                               thread_runner: endpoint.ThreadRunner,
                               sample_timestamp: str,
                               sample_salt: str,
                               sample_zipfile_signature: str,
                               sample_zipfile: io.BytesIO) -> None:

    post_return = test_client.post('/upload_file', data=dict(salt=sample_salt, signature=sample_zipfile_signature,
                                                             timestamp=sample_timestamp,
                                                             file=(sample_zipfile, 'zipfile')))
    assert post_return.status_code == HTTPStatus.OK
    thread_runner.join()
    check_file_in_azure(azure_service, azure_emulator_coords, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    for name, contents in zip(sample_filenames, sample_file_contents):
        check_file_in_azure(azure_service, azure_emulator_coords, name, contents)


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


def test_status_idle(test_client: testing.FlaskClient) -> None:
    status = test_client.get('/status')
    assert status.status_code == HTTPStatus.OK
    assert b'Endpoint: idle' in status.data


@pytest.mark.usefixtures('busy_thread_runner')
def test_status_busy(test_client: testing.FlaskClient) -> None:
    status = test_client.get('/status')
    assert status.status_code == HTTPStatus.OK
    assert b'Endpoint: busy' in status.data
