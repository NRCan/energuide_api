import io
import subprocess
import typing
import psutil
import pytest
import requests
import extract_post


class NamedStream(io.BytesIO):
    def __init__(self, *args, **kwargs):
        super(NamedStream, self).__init__(*args)
        self.name = kwargs['name']


@pytest.fixture(scope='session')
def test_host() -> str:
    return '127.0.0.1:5000'


@pytest.fixture()
def upload_url(test_host: str) -> str:
    return f'http://{test_host}/upload_file'


@pytest.fixture(scope='session')
def test_context(test_host: str) -> typing.Generator:
    proc = psutil.Popen(['python', 'src/extract_endpoint.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        try:
            requests.get(f'http://{test_host}/test_alive')
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


@pytest.mark.usefixtures('test_context')
def test_post_stream(upload_url: str, sample_stream: NamedStream, sample_filename: str) -> None:
    post_return = extract_post.post_stream(stream=sample_stream, filename=sample_filename, url=upload_url)
    assert post_return.status_code == 200


@pytest.mark.usefixtures('test_context')
def test_post_stream_stdin(upload_url: str, sample_stream_stdin: NamedStream, sample_filename: str) -> None:
    post_return = extract_post.post_stream(stream=sample_stream_stdin, filename=sample_filename, url=upload_url)
    assert post_return.status_code == 200


@pytest.mark.usefixtures('test_context')
def test_post_stream_no_filename(upload_url: str, sample_stream: NamedStream) -> None:
    post_return = extract_post.post_stream(stream=sample_stream, filename=None, url=upload_url)
    assert post_return.status_code == 200


@pytest.mark.usefixtures('test_context')
def test_post_stream_stdin_no_filename(upload_url: str, sample_stream_stdin: NamedStream) -> None:
    with pytest.raises(ValueError):
        extract_post.post_stream(stream=sample_stream_stdin, filename=None, url=upload_url)
