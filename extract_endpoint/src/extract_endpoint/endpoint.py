import os
import base64
import hashlib
import secrets
import typing
# import typing_extensions
from http import HTTPStatus
import zipfile
import requests
import flask
from werkzeug import utils
from azure.common import AzureMissingResourceHttpError
from extract_endpoint import azure_utils
from extract_endpoint import crypt_utils


DEFAULT_ENDPOINT_SECRET_KEY = 'no key'


TIMESTAMP_FILENAME = 'timestamp.txt'


App = flask.Flask(__name__)
App.config.update(dict(
    SECRET_KEY=os.environ.get('ENDPOINT_SECRET_KEY', DEFAULT_ENDPOINT_SECRET_KEY),
    AZURE_COORDINATES=azure_utils.StorageCoordinates(
        account=os.environ.get(azure_utils.EnvVariables.account.value, ''),
        key=os.environ.get(azure_utils.EnvVariables.key.value, ''),
        container=os.environ.get(azure_utils.EnvVariables.container.value, ''),
        domain=os.environ.get(azure_utils.EnvVariables.domain.value, None)
    )
))


@App.route('/', methods=['GET'])
def frontend() -> str:
    return ''


@App.route('/test_alive', methods=['GET'])
def test_alive() -> str:
    return 'Alive!'


@App.route('/robots933456.txt', methods=['GET'])
def robots() -> None:
    flask.abort(HTTPStatus.NOT_FOUND)


@App.route('/timestamp', methods=['GET'])
def timestamp() -> str:
    try:
        timestamp = azure_utils.download_bytes_from_azure(App.config['AZURE_COORDINATES'], TIMESTAMP_FILENAME)
    except AzureMissingResourceHttpError:
        flask.abort(HTTPStatus.BAD_GATEWAY)
    return timestamp


# class TriggerProtocol(typing_extensions.Protocol):
#
#     def send_to_trigger(self) -> requests.Response:
#         pass
#
#
# class ReadSendToTrigger:
#     def send_to_trigger(self, data:typing.Dict[str, str]) -> requests.Response:
#         return requests.post(os.environ['TRIGGER_URL'], data=data)
#
#
# class MockSendToTrigger:
#     def send_to_trigger(self, data:typing.Dict[str, str]) -> requests.Response:
#         response = requests.Response()
#         if 'salt' not in data:
#             response.status_code = HTTPStatus.BAD_REQUEST
#             response._content = b'no salt'
#             return response
#         if 'signature' not in data:
#             response.status_code = HTTPStatus.BAD_REQUEST
#             response._content = b'no signature'
#             return response
#
#         hasher = hashlib.new('sha3_256')
#         hasher.update((data['salt'] + App.config['SECRET_KEY']).encode())
#         actual_signature = hasher.hexdigest()
#         if data['signature'] != actual_signature:
#             response.status_code = HTTPStatus.BAD_REQUEST
#             response._content = b'bad signature'
#         else:
#             response.status_code = HTTPStatus.CREATED
#             response._content = b'success'
#         return response


def send_to_trigger(data: typing.Dict[str, str]) -> requests.Response:
    return requests.post(os.environ['TRIGGER_URL'], data=data)


def trigger(data: typing.Optional[typing.Dict[str, str]] = None) -> requests.Response:
    if data is None:
        salt = secrets.token_hex(16)
        hasher = hashlib.new('sha3_256')
        hasher.update((salt + App.config['SECRET_KEY']).encode())
        signature = hasher.hexdigest()
        data = dict(salt=salt, signature=signature)
    return send_to_trigger(data)


@App.route('/trigger_tl', methods=['POST'])
def trigger_tl() -> typing.Tuple[bytes, int]:
    trigger_response = trigger(data=flask.request.form)
    return b'', trigger_response.status_code


@App.route('/upload_file', methods=['POST'])
def upload_file() -> typing.Tuple[bytes, int]:
    if App.config['SECRET_KEY'] == DEFAULT_ENDPOINT_SECRET_KEY:
        raise ValueError("Need to define environment variable ENDPOINT_SECRET_KEY")
    if 'signature' not in flask.request.form:
        flask.abort(HTTPStatus.BAD_REQUEST)
    if 'salt' not in flask.request.form:
        flask.abort(HTTPStatus.BAD_REQUEST)
    if 'file' not in flask.request.files:
        flask.abort(HTTPStatus.BAD_REQUEST)
    if 'timestamp' not in flask.request.form:
        flask.abort(HTTPStatus.BAD_REQUEST)

    file = flask.request.files['file']
    signature = crypt_utils.sign_string(salt=flask.request.form['salt'], key=App.config['SECRET_KEY'],
                                        data=base64.b64encode(file.read()).decode('utf-8'))
    file.seek(0)
    if flask.request.form['signature'] != signature:
        flask.abort(HTTPStatus.BAD_REQUEST)

    try:
        file_z = zipfile.ZipFile(file)
    except zipfile.BadZipFile:
        return b"Bad Zipfile", HTTPStatus.BAD_REQUEST

    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        if not azure_utils.upload_bytes_to_azure(App.config['AZURE_COORDINATES'], json_file.read(),
                                                 utils.secure_filename(json_file.name)):
            flask.abort(HTTPStatus.BAD_GATEWAY)

    timestamp = flask.request.form['timestamp']

    if not azure_utils.upload_bytes_to_azure(App.config['AZURE_COORDINATES'], timestamp.encode(), TIMESTAMP_FILENAME):
        flask.abort(HTTPStatus.BAD_GATEWAY)

    trigger_response = trigger()
    return b'', trigger_response.status_code


if __name__ == "__main__":
    App.run(host='0.0.0.0')
