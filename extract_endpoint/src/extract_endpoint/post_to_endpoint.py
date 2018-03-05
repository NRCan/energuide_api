import os
import base64
import secrets
import typing
import requests
import click
from extract_endpoint import crypt_utils


DEFAULT_ENDPOINT_SECRET_KEY = 'no key'


@click.group()
def main() -> None:
    pass


def post_stream(stream: typing.IO[bytes],
                timestamp: str,
                url: str) -> requests.models.Response:

    data = stream.read()
    salt = secrets.token_hex(16)
    signature = crypt_utils.sign_string(salt=salt,
                                        key=os.environ.get('ENDPOINT_SECRET_KEY', DEFAULT_ENDPOINT_SECRET_KEY),
                                        data=base64.b64encode(data).decode('utf-8'))
    return requests.post(url=url,
                         files={'file': data},
                         data={'salt': salt, 'signature': signature, 'timestamp': timestamp})


@main.command()
@click.argument('stream', type=click.File('rb'))
@click.argument('timestamp')
@click.option('--url', default='http://127.0.0.1:5000/upload_file')
def upload(stream: typing.IO[bytes], timestamp: str, url: str) -> None:
    post_return = post_stream(stream=stream, timestamp=timestamp, url=url)
    click.echo(f"Response: {post_return.status_code}, {post_return.content}")
