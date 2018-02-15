import requests


ENDPOINT_URL = 'http://127.0.0.1:5000/upload_file'

ENDPOINT_SECRET_KEY = 'development_key'


def post_file(filename: str, url: str) -> str:
    with open(filename, 'rb') as file:
        retval = requests.post(url=url, files={'file': file}, data={'key': ENDPOINT_SECRET_KEY})
        return str(retval.content)


if __name__ == "__main__":
    Post_return_value = post_file('test.txt', url=ENDPOINT_URL)
    if 'success' in Post_return_value:
        print("Success")
    else:
        print(f"Error: {Post_return_value}")
