import os
import hashlib
import typing
from http import HTTPStatus
import zipfile
import flask
from werkzeug import utils
from azure.common import AzureMissingResourceHttpError
from extract_endpoint import azure_utils


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
    azure_service = azure_utils.AzureStorage(App.config['AZURE_COORDINATES'])

    try:
        timestamp = azure_utils.download_bytes_from_azure(azure_service, TIMESTAMP_FILENAME)
    except AzureMissingResourceHttpError:
        flask.abort(HTTPStatus.BAD_GATEWAY)
    return timestamp


@App.route('/upload_file', methods=['POST'])
def upload_file() -> typing.Tuple[str, int]:
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

    hasher = hashlib.new('sha3_256')
    hasher.update((flask.request.form['salt'] + App.config['SECRET_KEY']).encode())
    hasher.update(file.read())
    file.seek(0)
    signature = hasher.hexdigest()

    if flask.request.form['signature'] != signature:
        flask.abort(HTTPStatus.BAD_REQUEST)

    try:
        file_z = zipfile.ZipFile(file)
    except zipfile.BadZipFile:
        return "Bad Zipfile", HTTPStatus.BAD_REQUEST

    azure_service = azure_utils.AzureStorage(App.config['AZURE_COORDINATES'])

    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        if not azure_utils.upload_bytes_to_azure(azure_service, json_file.read(),
                                                 utils.secure_filename(json_file.name)):
            flask.abort(HTTPStatus.BAD_GATEWAY)

    timestamp = flask.request.form['timestamp']

    if not azure_utils.upload_bytes_to_azure(azure_service, timestamp.encode(), TIMESTAMP_FILENAME):
        flask.abort(HTTPStatus.BAD_GATEWAY)

    return 'success', HTTPStatus.CREATED


if __name__ == "__main__":
    App.run(host='0.0.0.0')
