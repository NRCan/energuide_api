import os
import base64
import flask
from werkzeug import utils
from extract_endpoint import azure_utils
from extract_endpoint import crypt_utils


DEFAULT_ENDPOINT_SECRET_KEY = 'no key'


App = flask.Flask(__name__)
App.config.update(dict(
    SECRET_KEY=os.environ.get('ENDPOINT_SECRET_KEY', DEFAULT_ENDPOINT_SECRET_KEY),
    AZURE_COORDINATES=azure_utils.StorageCoordinates(
        account=os.environ.get(azure_utils.EnvVariables.account.value, azure_utils.DefaultVariables.account.value),
        key=os.environ.get(azure_utils.EnvVariables.key.value, azure_utils.DefaultVariables.key.value),
        container=os.environ.get(azure_utils.EnvVariables.container.value,
                                 azure_utils.DefaultVariables.container.value),
        domain=os.environ.get(azure_utils.EnvVariables.domain.value, azure_utils.DefaultVariables.domain.value)
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
    flask.abort(404)


@App.route('/upload_file', methods=['POST'])
def upload_file() -> str:
    if App.config['SECRET_KEY'] == DEFAULT_ENDPOINT_SECRET_KEY:
        raise ValueError("Need to define environment variable ENDPOINT_SECRET_KEY")
    if 'signature' not in flask.request.form:
        flask.abort(404)
    if 'salt' not in flask.request.form:
        flask.abort(404)
    if flask.request.form.get('filename', '') == '':
        flask.abort(404)
    if 'file' not in flask.request.files:
        flask.abort(404)

    file = flask.request.files['file']
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    signature = crypt_utils.sign_string(salt=flask.request.form['salt'], key=App.config['SECRET_KEY'],
                                        data=file_as_string)
    if flask.request.form['signature'] != signature:
        flask.abort(404)

    file.seek(0)
    filename = utils.secure_filename(flask.request.form['filename'])
    if azure_utils.upload_stream_to_azure(App.config['AZURE_COORDINATES'], file, filename):
        return 'success'
    return 'failure'


if __name__ == "__main__":
    App.run()
