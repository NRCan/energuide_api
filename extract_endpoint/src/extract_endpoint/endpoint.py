import os
import base64
import typing
from http import HTTPStatus
import flask
from werkzeug import utils
from extract_endpoint import azure_utils
from extract_endpoint import crypt_utils


DEFAULT_ENDPOINT_SECRET_KEY = 'no key'


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
    print(flask.request.headers)
    return ''


@App.route('/test_alive', methods=['GET'])
def test_alive() -> str:
    print(flask.request.headers)
    return 'Alive!'


@App.route('/robots933456.txt', methods=['GET'])
def robots() -> None:
    print(flask.request.headers)
    flask.abort(HTTPStatus.NOT_FOUND)


@App.route('/upload_file', methods=['POST'])
def upload_file() -> typing.Tuple[str, int]:
    print(flask.request.headers)
    if App.config['SECRET_KEY'] == DEFAULT_ENDPOINT_SECRET_KEY:
        raise ValueError("Need to define environment variable ENDPOINT_SECRET_KEY")
    if 'signature' not in flask.request.form:
        flask.abort(HTTPStatus.BAD_REQUEST)
    if 'salt' not in flask.request.form:
        flask.abort(HTTPStatus.BAD_REQUEST)
    if flask.request.form.get('filename', '') == '':
        flask.abort(HTTPStatus.BAD_REQUEST)
    if 'file' not in flask.request.files:
        flask.abort(HTTPStatus.BAD_REQUEST)

    file = flask.request.files['file']
    file_contents = file.read()
    file_as_string = base64.b64encode(file_contents).decode('utf-8')
    signature = crypt_utils.sign_string(salt=flask.request.form['salt'], key=App.config['SECRET_KEY'],
                                        data=file_as_string)
    if flask.request.form['signature'] != signature:
        flask.abort(HTTPStatus.BAD_REQUEST)

    filename = utils.secure_filename(flask.request.form['filename'])

    if azure_utils.upload_bytes_to_azure(App.config['AZURE_COORDINATES'], file_contents, filename):
        return 'success', HTTPStatus.CREATED
    return 'failure', HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    App.run()
