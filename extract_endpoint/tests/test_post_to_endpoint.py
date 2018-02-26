import io
import subprocess
import typing
import psutil
import pytest
import _pytest
import requests
from azure.storage import blob
from extract_endpoint import post_to_endpoint, azure_utils


class NamedStream(io.BytesIO):
    def __init__(self, *args, **kwargs):
        super(NamedStream, self).__init__(*args)
        self.name = kwargs['name']


@pytest.fixture(scope='session')
def endpoint_host() -> str:
    return '127.0.0.1:5000'


@pytest.fixture()
def upload_url(endpoint_host: str) -> str:
    return f'http://{endpoint_host}/upload_file'


@pytest.fixture(scope='session')
def azure_service() -> blob.BlockBlobService:
    return blob.BlockBlobService(account_name=azure_utils.AZURE_EMULATOR_COORDS.account,
                                 account_key=azure_utils.AZURE_EMULATOR_COORDS.key,
                                 custom_domain=azure_utils.AZURE_EMULATOR_COORDS.domain)


@pytest.fixture(scope='session')
def test_context(azure_service: blob.BlockBlobService,
                 request: _pytest.fixtures.SubRequest,
                 endpoint_host: str) -> typing.Generator:

    azure_service.create_container(azure_utils.AZURE_EMULATOR_COORDS.container)

    monkeysession = _pytest.monkeypatch.MonkeyPatch()
    request.addfinalizer(monkeysession.undo)
    monkeysession.setenv('ENDPOINT_SECRET_KEY', 'endpoint secret key')
    monkeysession.setenv('EXTRACT_ENDPOINT_STORAGE_DOMAIN', azure_utils.AZURE_EMULATOR_COORDS.domain)

    proc = psutil.Popen(['python', 'src/extract_endpoint/endpoint.py'],
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        try:
            requests.get(f'http://{endpoint_host}/test_alive')
            break
        except requests.exceptions.ConnectionError:
            pass

    yield None

    proc.kill()
    azure_service.delete_container(azure_utils.AZURE_EMULATOR_COORDS.container)


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


def check_file_in_azure(azure_service: blob.BlockBlobService, filename: str, contents: str) -> None:
    assert filename in \
           [blob.name for blob in azure_service.list_blobs(azure_utils.AZURE_EMULATOR_COORDS.container)]
    actual_blob = azure_service.get_blob_to_text(azure_utils.AZURE_EMULATOR_COORDS.container, filename)
    assert actual_blob.content == contents


@pytest.mark.usefixtures('test_context')
def test_post_stream(azure_service: blob.BlockBlobService,
                     upload_url: str,
                     sample_stream: NamedStream,
                     sample_stream_content: str,
                     sample_filename: str) -> None:

    post_return = post_to_endpoint.post_stream(stream=sample_stream, filename=sample_filename, url=upload_url)
    assert post_return.status_code == 200

    check_file_in_azure(azure_service, sample_filename, sample_stream_content)


@pytest.mark.usefixtures('test_context')
def test_post_stream_stdin(azure_service: blob.BlockBlobService,
                           upload_url: str,
                           sample_stream_stdin: NamedStream,
                           sample_stream_content: str,
                           sample_filename: str) -> None:
    post_return = post_to_endpoint.post_stream(stream=sample_stream_stdin, filename=sample_filename, url=upload_url)
    assert post_return.status_code == 200
    check_file_in_azure(azure_service, sample_filename, sample_stream_content)


@pytest.mark.usefixtures('test_context')
def test_post_stream_no_filename(azure_service: blob.BlockBlobService,
                                 upload_url: str,
                                 sample_stream: NamedStream,
                                 sample_stream_content: str,
                                 sample_filename: str) -> None:
    post_return = post_to_endpoint.post_stream(stream=sample_stream, filename=None, url=upload_url)
    assert post_return.status_code == 200
    check_file_in_azure(azure_service, sample_filename, sample_stream_content)


@pytest.mark.usefixtures('test_context')
def test_post_stream_stdin_no_filename(upload_url: str, sample_stream_stdin: NamedStream) -> None:
    with pytest.raises(ValueError):
        post_to_endpoint.post_stream(stream=sample_stream_stdin, filename=None, url=upload_url)
