import os
import base64
import logging
from logging import handlers

import flask
from werkzeug import utils
import azure_utils
import crypt_utils


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


@App.route('/test_alive', methods=['GET'])
def frontend() -> str:
    return 'Alive!'


@App.route('/upload_file', methods=['POST'])
def upload_file() -> str:
    if App.config['SECRET_KEY'] == DEFAULT_ENDPOINT_SECRET_KEY:
        App.logger.error("Need to define environment variable ENDPOINT_SECRET_KEY")
        raise ValueError("Need to define environment variable ENDPOINT_SECRET_KEY")

    if 'signature' not in flask.request.form:
        App.logger.error("No signature sent")
        flask.abort(404)
    if 'salt' not in flask.request.form:
        App.logger.error("No salt sent")
        flask.abort(404)
    if flask.request.form.get('filename', '') == '':
        App.logger.error("Bad filename")
        flask.abort(404)
    if 'file' not in flask.request.files:
        App.logger.error("Bad file ")
        flask.abort(404)

    file = flask.request.files['file']
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    signature = crypt_utils.sign_string(salt=flask.request.form['salt'], key=App.config['SECRET_KEY'],
                                        data=file_as_string)
    if flask.request.form['signature'] != signature:
        App.logger.error(f"Sig sent {flask.request.form['signature']} != sig of file {signature}")
        flask.abort(404)

    file.seek(0)
    filename = utils.secure_filename(flask.request.form['filename'])
    if azure_utils.upload_stream_to_azure(App.config['AZURE_COORDINATES'], file, filename):
        App.logger.info(f"File {filename} uploaded to Azure")
        return 'success'
    App.logger.error(f"File {filename} failed upload to Azure")
    return 'failure'


if __name__ == "__main__":
    Formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    Handler = handlers.RotatingFileHandler('extract_endpoint.log', maxBytes=10000000, backupCount=1)
    Handler.setLevel(logging.DEBUG)
    App.logger.setLevel(logging.DEBUG)
    Handler.setFormatter(Formatter)
    App.logger.addHandler(Handler)
    App.run()
