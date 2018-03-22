import io
import subprocess
from http import HTTPStatus
import typing
import psutil
import pytest
import _pytest
import requests
from click import testing # type: ignore
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
def run_endpoint(monkeypatch: _pytest.monkeypatch.MonkeyPatch,
                 azure_emulator_coords: azure_utils.StorageCoordinates,
                 sample_secret_key: str,
                 endpoint_host: str) -> typing.Generator:

    monkeypatch.setenv('ETL_SECRET_KEY', sample_secret_key)
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', azure_emulator_coords.account)
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_KEY', azure_emulator_coords.key)
    monkeypatch.setenv('EXTRACT_ENDPOINT_CONTAINER', azure_emulator_coords.container)
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_DOMAIN', azure_emulator_coords.domain)
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


@pytest.mark.usefixtures('run_endpoint')
def test_post_stream_cli(sample_timestamp: str,
                         sample_zipfile_fixture: str,
                         upload_url: str) -> None:

    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'upload',
        sample_zipfile_fixture,
        sample_timestamp,
        '--url', upload_url
    ])
    assert result.exit_code != HTTPStatus.BAD_REQUEST


def test_etl_secret_key(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:
    assert post_to_endpoint._etl_secret_key() == post_to_endpoint.DEFAULT_ETL_SECRET_KEY
    monkeypatch.setenv('ETL_SECRET_KEY', 'test_key')
    assert post_to_endpoint._etl_secret_key() == 'test_key'


def test_endpoint_address(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:
    assert post_to_endpoint._endpoint_address() == post_to_endpoint.DEFAULT_ENERGUIDE_ENDPOINT_ADDRESS
    monkeypatch.setenv('ENERGUIDE_ENDPOINT_ADDRESS', 'test_address')
    assert post_to_endpoint._endpoint_address() == 'test_address'


def test_post_stream_cli_no_stream(upload_url: str, sample_timestamp: str) -> None:

    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'upload',
        None,
        sample_timestamp,
        '--url', upload_url
    ])
    assert result.exit_code != 0


def test_post_stream_cli_no_timestamp(sample_zipfile_fixture: str, upload_url: str) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'upload',
        sample_zipfile_fixture,
        None,
        '--url', upload_url
    ])
    assert result.exit_code != 0


@pytest.mark.usefixtures('run_endpoint')
def test_post_stream_cli_no_url(sample_timestamp: str,
                                sample_zipfile_fixture: str) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'upload',
        sample_zipfile_fixture,
        sample_timestamp,
        '--url', None
    ])
    assert result.exit_code != HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('run_endpoint')
def test_run_tl() -> None:
    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'run_tl',
        '--url', None
    ])
    assert result.exit_code != HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('run_endpoint')
def test_status() -> None:
    runner = testing.CliRunner()
    result = runner.invoke(post_to_endpoint.main, args=[
        'status',
        '--url', None
    ])

    assert result.exit_code == 0
    assert 'System Status' in result.output
