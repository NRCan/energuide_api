import os
import hashlib
import secrets
import typing
from http import HTTPStatus
import requests
import click


DEFAULT_ETL_SECRET_KEY = 'no key'


def _etl_secret_key() -> str:
    return os.environ.get('ETL_SECRET_KEY', DEFAULT_ETL_SECRET_KEY)


@click.group()
def main() -> None:
    pass


def post_stream(stream: typing.IO[bytes],
                timestamp: str,
                url: str) -> requests.models.Response:

    data = stream.read()
    salt = secrets.token_hex(16)

    hasher = hashlib.new('sha3_256')
    hasher.update((salt + _etl_secret_key()).encode())
    hasher.update(data)
    signature = hasher.hexdigest()

    return requests.post(url=url,
                         files={'file': data},
                         data={'salt': salt, 'signature': signature, 'timestamp': timestamp})


def send_to_tl_app(url: str, data: typing.Dict[str, str]) -> int:
    return requests.post(url, data=data).status_code


def trigger_tl(url) -> int:
    salt = secrets.token_hex(16)
    hasher = hashlib.new('sha3_256')
    hasher.update((salt + _etl_secret_key()).encode())
    signature = hasher.hexdigest()
    data = dict(salt=salt, signature=signature)
    return send_to_tl_app(url, data)


@main.command()
@click.argument('stream', type=click.File('rb'))
@click.argument('timestamp')
@click.option('--url', default='http://127.0.0.1:5000/upload_file')
def upload(stream: typing.IO[bytes], timestamp: str, url: str) -> None:
    post_return = post_stream(stream=stream, timestamp=timestamp, url=url)
    click.echo(f"Response: {post_return.status_code}, {post_return.content}")


@main.command()
@click.option('--url', default='http://127.0.0.1:5000/run_tl')
def run_tl(url: str) -> None:
    trigger_return_code = trigger_tl(url)
    click.echo(f"Response: {trigger_return_code}")
    if trigger_return_code != HTTPStatus.OK:
        exit(trigger_return_code)
