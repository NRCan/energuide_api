"""
Flask microservice demo. When a file is posted to it, save the file locally.
"""

import os

from flask import Flask, request, abort
from werkzeug.utils import secure_filename
from azure_storage import EnvDefaults, EnvVariables, StorageCoordinates, \
    upload_stream_to_azure

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

App = Flask(__name__)

App.config.update(dict(
    SECRET_KEY='development_key',
    UPLOAD_FOLDER='Uploads',
))
App.config.from_envvar('EXTRACT_ENDPOINT', silent=True)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# this is a just a helper page that can also post to the service
@App.route('/frontend', methods=['GET'])
def frontend() -> str:
    return f"""
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="upload_file" method=post enctype=multipart/form-data>
      <p><input type=text name=key value="{App.config['SECRET_KEY']}"><br>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """


# this is the upload service view
@App.route('/upload_file', methods=['POST'])
def upload_file() -> str:
    if App.debug:
        if 'key' not in request.form:
            return "Error: no key sent"
        elif request.form['key'] != App.config['SECRET_KEY']:
            return "Error: bad key sent"

    if 'key' not in request.form or request.form['key'] != App.config['SECRET_KEY']:
        abort(404)

    # check if the post request has the file part
    if 'file' not in request.files:
        return "Error: no file"

    file = request.files['file']

    # make sure the file has a filename
    if file.filename == '':
        return "Error: file does not have a filename"

    if not allowed_file(file.filename):
        return f"Error: file extension of '{file.filename}' not allowed"

    # a valid file was posted
    filename = secure_filename(file.filename)

    account = os.environ.get(EnvVariables.account.value, EnvDefaults.account.value)
    key = os.environ.get(EnvVariables.key.value, EnvDefaults.key.value)
    container = os.environ.get(EnvVariables.container.value, EnvDefaults.container.value)
    domain = os.environ.get(EnvVariables.domain.value, EnvDefaults.domain.value)

    azure_sc = StorageCoordinates(account, key, container, domain)

    return upload_stream_to_azure(azure_sc, file, filename)


if __name__ == "__main__":
    App.run()
