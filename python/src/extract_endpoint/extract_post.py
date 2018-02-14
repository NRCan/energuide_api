import requests


filename = 'test.txt'
url = 'http://127.0.0.1:5000/upload_file'

ENDPOINT_SECRET_KEY = 'development key'

with open(filename, 'rb') as f:
    r = requests.post(url=url, files={'file': f}, data={'key': ENDPOINT_SECRET_KEY})
    print(r.content)
