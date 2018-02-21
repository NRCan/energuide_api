import io
import os
import base64
import secrets
import requests
import click
import typing
from crypt_utils import sign_string


def post_file(stream: typing.IO[bytes], filename: str, url: str) -> requests.models.Response:
    if filename is None and stream.name == '<stdin>':
        raise ValueError("must have a filename if reading from stdin")
    if filename is None:
        filename = stream.name
    memory_stream = io.BytesIO(stream.read())

    salt = secrets.token_hex(16)
    signature = sign_string(salt=salt, key=os.environ.get('ENDPOINT_SECRET_KEY', ''),
                            data=base64.b64encode(memory_stream.read()).decode('utf-8'))
    memory_stream.seek(0)
    return requests.post(url=url,
                         files={'file': memory_stream},
                         data={'salt': salt, 'signature': signature, 'filename': filename})

@click.command()
@click.argument('stream', type=click.File('rb'))
@click.option('--filename')
@click.option('--url', default='http://127.0.0.1:5000/upload_file')
def main(stream: typing.IO[bytes], filename: str, url: str) -> None:
    print(f'POST returned: {post_file(stream=stream, filename=filename, url=url)}')


if __name__ == "__main__":
    main()
