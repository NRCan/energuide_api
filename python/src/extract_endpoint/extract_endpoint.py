"""
Flask microservice demo. When a file is posted to it, save the file locally.
"""

import os
import base64
from flask import Flask, request, abort
from werkzeug.utils import secure_filename
from azure_utils import EnvDefaults, EnvVariables, StorageCoordinates, upload_stream_to_azure
from crypt_utils import sign_data


DEFAULT_ENDPOINT_SECRET_KEY = 'no key'

App = Flask(__name__)
App.debug = False
App.config.update(dict(
    SECRET_KEY=os.environ.get('ENDPOINT_SECRET_KEY', DEFAULT_ENDPOINT_SECRET_KEY),
))


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
    if App.config['SECRET_KEY'] == DEFAULT_ENDPOINT_SECRET_KEY:
        raise ValueError("Need to define environment variable ENDPOINT_SECRET_KEY")

    if App.debug:
        if 'signature' not in request.form:
            return "Error: no signature sent"
        elif 'salt' not in request.form:
            return "Error: no salt sent"
    else:
        if 'signature' not in request.form or 'salt' not in request.form:
            abort(404)

    # check if the post request has a file and filename
    if 'file' not in request.files or getattr(request.files['file'], 'filename', '') == '':
        if App.debug:
            return "Error: bad file"
        else:
            abort(404)

    file = request.files['file']

    # check that the signature is valid
    file_as_string = base64.b64encode(file.read()).decode('utf-8')
    signed_file = sign_data(salt=request.form['salt'], key=App.config['SECRET_KEY'], data=file_as_string)
    if request.form['signature'] != signed_file:
        if App.debug:
            return f"Sig sent: {request.form['signature']} != {signed_file}"
        else:
            abort(404)

    file.seek(0)
    filename = secure_filename(file.filename)
    account = os.environ.get(EnvVariables.account.value, EnvDefaults.account.value)
    key = os.environ.get(EnvVariables.key.value, EnvDefaults.key.value)
    container = os.environ.get(EnvVariables.container.value, EnvDefaults.container.value)
    domain = os.environ.get(EnvVariables.domain.value, EnvDefaults.domain.value)
    azure_sc = StorageCoordinates(account, key, container, domain)
    return upload_stream_to_azure(azure_sc, file, filename)


if __name__ == "__main__":
    App.run()
