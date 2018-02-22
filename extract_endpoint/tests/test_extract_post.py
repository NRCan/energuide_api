import io
import subprocess
import psutil
import pytest
import requests
import extract_post


class NamedStream(io.BytesIO):
    def __init__(self, *args, **kwargs):
        super(NamedStream, self).__init__(*args)
        self.name = kwargs['name']


class TestContext():

    hostname = '127.0.0.1:5000'
    upload_url = f'http://{hostname}/upload_file'
    test_alive_url = f'http://{hostname}/test_alive'
    proc: psutil.Popen

    def create(self) -> None:
        self.proc = psutil.Popen(['python', 'src/extract_endpoint.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        while True:
            try:
                requests.get(self.test_alive_url)
                break
            except requests.exceptions.ConnectionError:
                pass

    def tear_down(self) -> None:
        self.proc.kill()


@pytest.fixture(scope='session')
def test_context():
    context = TestContext()
    context.create()
    yield context
    context.tear_down()


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


def test_post_stream(test_context: TestContext,
                     sample_stream: NamedStream,
                     sample_filename: str) -> None:

    post_return = extract_post.post_stream(stream=sample_stream, filename=sample_filename, url=test_context.upload_url)
    assert post_return.status_code == 200


def test_post_stream_stdin(test_context: TestContext,
                           sample_stream_stdin: NamedStream,
                           sample_filename: str) -> None:

    post_return = extract_post.post_stream(stream=sample_stream_stdin, filename=sample_filename,
                                           url=test_context.upload_url)
    assert post_return.status_code == 200


def test_post_stream_no_filename(test_context: TestContext,
                                 sample_stream: NamedStream) -> None:

    post_return = extract_post.post_stream(stream=sample_stream, filename=None, url=test_context.upload_url)
    assert post_return.status_code == 200


def test_post_stream_stdin_no_filename(test_context: TestContext,
                                       sample_stream_stdin: NamedStream) -> None:

    with pytest.raises(ValueError):
        extract_post.post_stream(stream=sample_stream_stdin, filename=None, url=test_context.upload_url)
