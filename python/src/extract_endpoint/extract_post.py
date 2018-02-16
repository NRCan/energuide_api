import os
import requests
import click

ENDPOINT_URL = 'http://127.0.0.1:5000/upload_file'


def post_file(filename: str, url: str) -> str:
    with open(filename, 'rb') as file:
        retval = requests.post(url=url, files={'file': file},
                               data={'key': os.environ.get('ENDPOINT_SECRET_KEY')})
        return str(retval.content)


@click.command()
@click.option('--filename', type=click.Path(exists=True), required=True)
def main(filename='test.txt'):
    post_return_value = post_file(filename, url=ENDPOINT_URL)
    if 'success' in post_return_value.lower():
        print(f"Success: {post_return_value}")
    else:
        print(f"Error: {post_return_value}")


if __name__ == "__main__":
    main()
