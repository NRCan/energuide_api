import os
import shutil
from io import BytesIO
from extract_endpoint import extract_endpoint

CONTENTS = 'my file contents'.encode('utf-8')


extract_endpoint.App.testing = True


def test_frontend() -> None:
    app = extract_endpoint.App.test_client()
    actual = app.get('/frontend')
    assert b'Upload new File' in actual.data


def test_upload() -> None:
    os.mkdir('Uploads')
    app = extract_endpoint.App.test_client()

    actual = app.post('/upload_file',
                      data=dict(key='development_key',
                                file=(BytesIO(CONTENTS), 'hello world.txt')))

    shutil.rmtree('Uploads')
    assert actual.data == b'hello_world.txt uploaded successfully'
