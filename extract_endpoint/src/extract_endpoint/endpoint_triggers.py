import typing
import hashlib
import secrets
from http import HTTPStatus
import zipfile
import requests
import typing_extensions
from werkzeug import utils
from extract_endpoint import azure_utils


SAMPLE_FILENAME = "sample_file.txt"


class EndpointTrigger(typing_extensions.Protocol):

    def run_count(self) -> int:
        pass

    def run(self) -> int:
        pass


class MockUploadToAzure(EndpointTrigger):
    def __init__(self, data: typing.IO[bytes], timestamp: str, timestamp_filename: str) -> None:
        self._data = data
        self._timestamp = timestamp
        self._timestamp_filename = timestamp_filename
        self._run_count = 0

    @property
    def run_count(self) -> int:
        return self._run_count

    def run(self) -> int:
        mock_service = azure_utils.MockStorage()
        self._run_count += 1
        return upload_to_storage(mock_service, self._data, self._timestamp, self._timestamp_filename)


class MockTriggerTL(EndpointTrigger):
    def __init__(self, key: str, url: str, data: typing.Optional[typing.Dict[str, str]] = None) -> None:
        self._run_count = 0
        self._key = key
        self._url = url
        if data is None:
            salt = secrets.token_hex(16)
            hasher = hashlib.new('sha3_256')
            hasher.update((salt + self._key).encode())
            signature = hasher.hexdigest()
            self._data = dict(salt=salt, signature=signature)
        else:
            self._data = data

    @property
    def run_count(self) -> int:
        return self._run_count

    def run(self) -> int:
        self._run_count += 1

        if 'salt' not in self._data:
            return HTTPStatus.BAD_REQUEST
        if 'signature' not in self._data:
            return HTTPStatus.BAD_REQUEST
        hasher = hashlib.new('sha3_256')
        hasher.update((self._data['salt'] + self._key).encode())
        actual_signature = hasher.hexdigest()
        if self._data['signature'] != actual_signature:
            return HTTPStatus.BAD_REQUEST
        return HTTPStatus.CREATED


class UploadFilesToAzure(EndpointTrigger):
    def __init__(self, data: typing.IO[bytes],
                 timestamp: str,
                 timestamp_filename: str,
                 coords: azure_utils.StorageCoordinates) -> None:

        self._data = data
        self._coords = coords
        self._timestamp = timestamp
        self._timestamp_filename = timestamp_filename

    def run(self) -> int:
        azure_service = azure_utils.AzureStorage(self._coords)
        return upload_to_storage(azure_service, self._data, self._timestamp, self._timestamp_filename)


class TriggerTL(EndpointTrigger):
    def __init__(self, key: str, url: str, data: typing.Optional[typing.Dict[str, str]] = None) -> None:
        self._key = key
        self._url = url
        if data is None:
            salt = secrets.token_hex(16)
            hasher = hashlib.new('sha3_256')
            hasher.update((salt + self._key).encode())
            signature = hasher.hexdigest()
            self._data = dict(salt=salt, signature=signature)
        else:
            self._data = data

    def run(self) -> int:
        return requests.post(self._url, data=self._data).status_code


def upload_to_storage(storage_service: azure_utils.StorageProtocol,
                      data: typing.IO[bytes],
                      timestamp: str,
                      timestamp_filename: str) -> int:
    try:
        file_z = zipfile.ZipFile(data)
    except zipfile.BadZipFile:
        return HTTPStatus.BAD_REQUEST

    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        if not storage_service.upload(json_file.read(), utils.secure_filename(json_file.name)):
            return HTTPStatus.BAD_GATEWAY

    if not storage_service.upload(timestamp.encode(), timestamp_filename):
        return HTTPStatus.BAD_GATEWAY

    return HTTPStatus.CREATED
