import requests
import click

ENDPOINT_URL = 'http://127.0.0.1:5000/upload_file'

ENDPOINT_SECRET_KEY = 'development_key'


def post_file(filename: str, url: str) -> str:
    with open(filename, 'rb') as file:
        retval = requests.post(url=url, files={'file': file}, data={'key': ENDPOINT_SECRET_KEY})
        return str(retval.content)


@click.command()
@click.argument('filename')
def main(filename: str):
    Post_return_value = post_file(filename, url=ENDPOINT_URL)
    if 'success' in Post_return_value.lower():
        print(f"Success: {Post_return_value}")
    else:
        print(f"Error: {Post_return_value}")


if __name__ == "__main__":
    main()
