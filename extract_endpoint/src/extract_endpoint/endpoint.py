import os
import hashlib
import secrets
import typing
from http import HTTPStatus
import zipfile
import requests
import flask
from werkzeug import utils
from azure.common import AzureMissingResourceHttpError
from extract_endpoint import azure_utils
from extract_endpoint import logger


LOGGER = logger.get_logger(__name__)


DEFAULT_ETL_SECRET_KEY = 'no key'


TIMESTAMP_FILENAME = 'timestamp.txt'


App = flask.Flask(__name__)
App.config.update(dict(
    SECRET_KEY=os.environ.get('ETL_SECRET_KEY', DEFAULT_ETL_SECRET_KEY),
    AZURE_COORDINATES=azure_utils.StorageCoordinates(
        account=os.environ.get(azure_utils.EnvVariables.account.value, ''),
        key=os.environ.get(azure_utils.EnvVariables.key.value, ''),
        container=os.environ.get(azure_utils.EnvVariables.container.value, ''),
        domain=os.environ.get(azure_utils.EnvVariables.domain.value, None)
    )
))


def _trigger_url() -> str:
    return os.environ.get('TRIGGER_ADDRESS', 'http://0.0.0.0:5010') + '/run_tl'


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
    LOGGER.info("Fetching timestamp")
    try:
        timestamp = azure_utils.download_bytes_from_azure(App.config['AZURE_COORDINATES'], TIMESTAMP_FILENAME)
    except AzureMissingResourceHttpError as exc:
        LOGGER.warning(f"Error contacting Azure: {logger.unwrap_exception_message(exc)}")
        flask.abort(HTTPStatus.BAD_GATEWAY)
    return timestamp


def send_to_trigger(data: typing.Dict[str, str]) -> int:
    LOGGER.info("Telling TL to start")
    return requests.post(_trigger_url(), data=data).status_code


def trigger(data: typing.Optional[typing.Dict[str, str]] = None) -> int:
    if data is None:
        salt = secrets.token_hex(16)
        hasher = hashlib.new('sha3_256')
        hasher.update((salt + App.config['SECRET_KEY']).encode())
        signature = hasher.hexdigest()
        data = dict(salt=salt, signature=signature)
    return send_to_trigger(data)


@App.route('/trigger_tl', methods=['POST'])
def trigger_tl() -> typing.Tuple[str, int]:
    if flask.request.form is None or any(key not in flask.request.form for key in ['signature', 'salt']):
        LOGGER.warning("Missing salt or signature in trigger request")
        flask.abort(HTTPStatus.BAD_REQUEST)
    return '', trigger(data=flask.request.form)


@App.route('/upload_file', methods=['POST'])
def upload_file() -> typing.Tuple[str, int]:
    LOGGER.info("Received upload request")
    if App.config['SECRET_KEY'] == DEFAULT_ETL_SECRET_KEY:
        LOGGER.error("Need to define environment variable ETL_SECRET_KEY")
        raise ValueError("Need to define environment variable ETL_SECRET_KEY")
    if flask.request.form is None \
            or any(key not in flask.request.form for key in ['signature', 'salt', 'timestamp']) \
            or 'file' not in flask.request.files:
        LOGGER.warning("Missing signature, salt, or timestamp")
        flask.abort(HTTPStatus.BAD_REQUEST)

    file = flask.request.files['file']

    hasher = hashlib.new('sha3_256')
    hasher.update((flask.request.form['salt'] + App.config['SECRET_KEY']).encode())
    hasher.update(file.read())
    file.seek(0)
    signature = hasher.hexdigest()

    if flask.request.form['signature'] != signature:
        LOGGER.warning("Bad signature")
        flask.abort(HTTPStatus.BAD_REQUEST)

    try:
        file_z = zipfile.ZipFile(file)
    except zipfile.BadZipFile:
        LOGGER.warning("Bad zipfile")
        return "Bad Zipfile", HTTPStatus.BAD_REQUEST

    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        if not azure_utils.upload_bytes_to_azure(App.config['AZURE_COORDINATES'], json_file.read(),
                                                 utils.secure_filename(json_file.name)):
            LOGGER.warning("File upload to Azure storage failed")
            flask.abort(HTTPStatus.BAD_GATEWAY)
    LOGGER.info(f"{len(file_z.infolist())} json files uploaded to Azure")

    timestamp = flask.request.form['timestamp']
    if not azure_utils.upload_bytes_to_azure(App.config['AZURE_COORDINATES'], timestamp.encode(), TIMESTAMP_FILENAME):
        LOGGER.warning("Timestamp upload to Azure storage failed")
        flask.abort(HTTPStatus.BAD_GATEWAY)

    return '', trigger()


if __name__ == "__main__":
    App.run(host='0.0.0.0')
