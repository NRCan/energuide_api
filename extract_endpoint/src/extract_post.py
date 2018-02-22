import io
import os
import base64
import secrets
import typing
import requests
import click
from crypt_utils import sign_string


DEFAULT_ENDPOINT_SECRET_KEY = 'endpoint_secret_key'


@click.group()
def main() -> None:
    pass


def post_stream(stream: typing.IO[bytes], filename: typing.Optional[str], url: str) -> requests.models.Response:
    if filename is None and stream.name == '<stdin>':
        raise ValueError("must have a filename if reading from stdin")
    if filename is None:
        filename = stream.name
    memory_stream = io.BytesIO(stream.read())

    salt = secrets.token_hex(16)
    signature = sign_string(salt=salt, key=os.environ.get('ENDPOINT_SECRET_KEY', DEFAULT_ENDPOINT_SECRET_KEY),
                            data=base64.b64encode(memory_stream.read()).decode('utf-8'))
    memory_stream.seek(0)
    return requests.post(url=url,
                         files={'file': memory_stream},
                         data={'salt': salt, 'signature': signature, 'filename': filename})


@main.command()
@click.argument('stream', type=click.File('rb'))
@click.option('--filename')
@click.option('--url', default='http://127.0.0.1:5000/upload_file')
def upload(stream: typing.IO[bytes], filename: typing.Optional[str], url: str) -> requests.models.Response:
    return post_stream(stream=stream, filename=filename, url=url)
