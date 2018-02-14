import requests


filename = 'test.txt'
url = 'http://127.0.0.1:5000/upload_file'


with open(filename, 'rb') as f:
    r = requests.post(url=url, files={'file': f})
    print(r.content)
