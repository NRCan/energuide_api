import io
import subprocess
import psutil
import pytest
import requests
import extract_post
import time
import typing

class NamedStream(io.BytesIO):
    def __init__(self, *args, **kwargs):
        super(NamedStream, self).__init__(*args)
        self.name = kwargs['name']


@pytest.fixture
def post_stream():
    proc = psutil.Popen(['python', 'src/extract_endpoint.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(0.5)
    yield extract_post.post_stream
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
def sample_url() -> str:
    return 'http://127.0.0.1:5000/upload_file'


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


def test_post_stream(post_stream, sample_stream: NamedStream, sample_filename: str, sample_url: str) -> None:
    post_return = post_stream(stream=sample_stream, filename=sample_filename, url=sample_url)
    assert post_return.status_code == 200


def test_post_stream_stdin(post_stream, sample_stream_stdin: NamedStream, sample_filename: str, sample_url: str) -> None:
    post_return = post_stream(stream=sample_stream_stdin, filename=sample_filename, url=sample_url)
    assert post_return.status_code == 200


def test_post_stream_no_filename(post_stream, sample_stream: NamedStream, sample_url: str) -> None:
    post_return = post_stream(stream=sample_stream, filename=None, url=sample_url)
    assert post_return.status_code == 200


def test_post_stream_stdin_no_filename(sample_stream_stdin: NamedStream, sample_url: str) -> None:
    with pytest.raises(ValueError):
        extract_post.post_stream(stream=sample_stream_stdin, filename=None, url=sample_url)


def test_post_stream_bad_url(sample_stream: NamedStream, sample_filename: str) -> None:
    with pytest.raises(requests.exceptions.ConnectionError):
        extract_post.post_stream(stream=sample_stream, filename=sample_filename, url='http://bad_url')


def test_post_stream_invalid_url(sample_stream: NamedStream, sample_filename: str) -> None:
    with pytest.raises(requests.exceptions.MissingSchema):
        extract_post.post_stream(stream=sample_stream, filename=sample_filename, url='not a url')


def test_post_stream_no_stream(sample_filename: str, sample_url: str) -> None:
    with pytest.raises(AttributeError):
        extract_post.post_stream(stream=None, filename=sample_filename, url=sample_url)
