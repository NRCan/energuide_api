import io
import subprocess
import typing
from http import HTTPStatus
import psutil
import pytest
import _pytest
import requests
from azure.storage import blob
from extract_endpoint import post_to_endpoint, azure_utils, endpoint


class NamedStream(io.BytesIO):
    name: str

    def __init__(self, *args, **kwargs) -> None:
        super(NamedStream, self).__init__(*args)
        self.name = kwargs['name']


@pytest.fixture(scope='session')
def endpoint_host() -> str:
    return '127.0.0.1:5000'


@pytest.fixture()
def upload_url(endpoint_host: str) -> str:
    return f'http://{endpoint_host}/upload_file'


@pytest.fixture()
def run_endpoint(azure_emulator_coords: azure_utils.StorageCoordinates,
                 sample_secret_key: str,
                 request: _pytest.fixtures.SubRequest,
                 endpoint_host: str) -> typing.Generator:

    monkeysession = _pytest.monkeypatch.MonkeyPatch()
    request.addfinalizer(monkeysession.undo)
    monkeysession.setenv('ENDPOINT_SECRET_KEY', sample_secret_key)
    monkeysession.setenv('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', azure_emulator_coords.account)
    monkeysession.setenv('EXTRACT_ENDPOINT_STORAGE_KEY', azure_emulator_coords.key)
    monkeysession.setenv('EXTRACT_ENDPOINT_CONTAINER', azure_emulator_coords.container)
    monkeysession.setenv('EXTRACT_ENDPOINT_STORAGE_DOMAIN', azure_emulator_coords.domain)

    proc = psutil.Popen(['python', 'src/extract_endpoint/endpoint.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        try:
            requests.get(f'http://{endpoint_host}/test_alive')
            break
        except requests.exceptions.ConnectionError:
            pass

    yield None

    proc.kill()


@pytest.fixture
def sample_stream_content() -> str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content: str, sample_filename: str) -> NamedStream:
    return NamedStream(sample_stream_content.encode(), name=sample_filename)


@pytest.fixture
def sample_stream_stdin(sample_stream_content: str) -> NamedStream:
    return NamedStream(sample_stream_content.encode(), name='<stdin>')


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


@pytest.fixture
def sample_timestamp_filename() -> str:
    return endpoint.TIMESTAMP_FILENAME


def check_file_in_azure(azure_service: blob.BlockBlobService,
                        azure_emulator_coords: azure_utils.StorageCoordinates,
                        filename: str,
                        contents: str) -> None:

    assert filename in [blob.name for blob in azure_service.list_blobs(azure_emulator_coords.container)]
    actual_blob = azure_service.get_blob_to_text(azure_emulator_coords.container, filename)
    assert actual_blob.content == contents


@pytest.mark.usefixtures('mocked_tl_app', 'run_endpoint')
def test_post_stream(azure_service: blob.BlockBlobService,
                     azure_emulator_coords: azure_utils.StorageCoordinates,
                     upload_url: str,
                     sample_timestamp: str,
                     sample_file_contents: str,
                     sample_filenames: str,
                     sample_zipfile: io.BytesIO) -> None:

    post_return = post_to_endpoint.post_stream(stream=sample_zipfile, filename="filename",
                                               timestamp=sample_timestamp, url=upload_url)
    assert post_return.status_code == HTTPStatus.CREATED
    check_file_in_azure(azure_service, azure_emulator_coords, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    for name, contents in zip(sample_filenames, sample_file_contents):
        check_file_in_azure(azure_service, azure_emulator_coords, name, contents)


@pytest.mark.usefixtures('run_endpoint')
def test_post_stream_stdin(azure_service: blob.BlockBlobService,
                           azure_emulator_coords: azure_utils.StorageCoordinates,
                           upload_url: str,
                           sample_timestamp: str,
                           sample_file_contents: str,
                           sample_filenames: str,
                           sample_zipfile: io.BytesIO) -> None:
    post_return = post_to_endpoint.post_stream(stream=sample_zipfile, filename="filename",
                                               timestamp=sample_timestamp, url=upload_url)
    assert post_return.status_code == HTTPStatus.CREATED
    check_file_in_azure(azure_service, azure_emulator_coords, endpoint.TIMESTAMP_FILENAME, sample_timestamp)
    for name, contents in zip(sample_filenames, sample_file_contents):
        check_file_in_azure(azure_service, azure_emulator_coords, name, contents)
