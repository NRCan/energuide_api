import os
import base64
import requests
import click
from crypt_utils import get_salt, sign_string


ENDPOINT_URL = 'http://127.0.0.1:5000/upload_file'


def post_file(filename: str, url: str) -> str:
    salt = get_salt()
    with open(filename, 'rb') as file:
        file_as_string = base64.b64encode(file.read()).decode('utf-8')
        file.seek(0)
        signature = sign_string(salt=salt, key=os.environ.get('ENDPOINT_SECRET_KEY'), data=file_as_string)

        retval = requests.post(url=url, files={'file': file},
                               data={'salt': salt, 'signature': signature})
        return str(retval.content)


@click.command()
@click.option('--filename', type=click.Path(exists=True), required=True)
def main(filename='test.txt') -> None:

    print()
    post_return_value = post_file(filename, url=ENDPOINT_URL)
    if 'success' in post_return_value.lower():
        print(f"Success: {post_return_value}")
    else:
        print(f"Error: {post_return_value}")


if __name__ == "__main__":
    main()
