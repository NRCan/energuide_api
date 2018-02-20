import os
import base64
import secrets
import requests
import click
from crypt_utils import sign_string


ENDPOINT_URL = 'http://127.0.0.1:5000/upload_file'


def post_file(filename: str, url: str) -> str:
    salt = secrets.token_hex(16)
    with open(filename, 'rb') as file:
        file_as_string = base64.b64encode(file.read()).decode('utf-8')
        file.seek(0)
        signature = sign_string(salt=salt, key=os.environ.get('ENDPOINT_SECRET_KEY', ''), data=file_as_string)

        retval = requests.post(url=url, files={'file': file},
                               data={'salt': salt, 'signature': signature})
        return str(retval.content)


@click.command()
@click.option('--filename', type=click.Path(exists=True), required=True)
def main(filename='test.txt') -> None:
    print(f'POST returned: {post_file(filename, url=ENDPOINT_URL)}')


if __name__ == "__main__":
    main()
