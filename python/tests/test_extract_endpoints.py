import os
import shutil
from io import BytesIO
from extract_endpoint import extract_endpoint
from azure_storage import EnvVariables, EnvDefaults
from azure.storage.blob import BlockBlobService


CONTENTS = 'test_contents'
TEST_FILENAME = 'test_blob_filename_989.txt'


extract_endpoint.App.testing = True


def test_frontend() -> None:
    app = extract_endpoint.App.test_client()
    actual = app.get('/frontend')
    assert b'Upload new File' in actual.data


def test_upload_no_key() -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(CONTENTS.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(file=(stream, TEST_FILENAME)))
    assert actual.status_code == 404


def test_upload_wrong_key() -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(CONTENTS.encode('utf-8'))
    actual = app.post('/upload_file', data=dict(key='bad key', file=(stream, TEST_FILENAME)))
    assert actual.status_code == 404


def test_upload() -> None:
    app = extract_endpoint.App.test_client()
    stream = BytesIO(CONTENTS.encode('utf-8'))
    app.post('/upload_file', data=dict(key='development_key', file=(stream, TEST_FILENAME)))

    account = os.environ.get(EnvVariables.account.value, EnvDefaults.account.value)
    key = os.environ.get(EnvVariables.key.value, EnvDefaults.key.value)
    container = os.environ.get(EnvVariables.container.value, EnvDefaults.container.value)
    domain = os.environ.get(EnvVariables.domain.value, EnvDefaults.domain.value)
    block_blob_service = BlockBlobService(account_name=account, account_key=key, custom_domain=domain)
    assert TEST_FILENAME in [blob.name for blob in block_blob_service.list_blobs(container)]
    actual = block_blob_service.get_blob_to_text(container, TEST_FILENAME)
    block_blob_service.delete_blob(container, TEST_FILENAME)
    assert actual.content == CONTENTS
