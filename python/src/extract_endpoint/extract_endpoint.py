"""
Flask microservice demo. When a file is posted to it, save the file locally.
"""

import os

from flask import Flask, request, render_template, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

App = Flask(__name__)

App.config.update(dict(
    SECRET_KEY='development key',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
))
App.config.from_envvar('EXTRACT_ENDPOINT', silent=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# this is a just a helper page that can also post to the service
@App.route('/frontend', methods=['GET'])
def frontend():
    print(request)
    return render_template('frontend.html')


# this is the upload service view
@App.route('/upload_file', methods=['POST'])
def upload_file():
    print(request)
    if 'key' not in request.form or request.form['key'] != App.config['SECRET_KEY']:
        abort(404)

    # check if the post request has the file part
    if 'file' not in request.files:
        return render_template('error.html', error='No file')

    file = request.files['file']

    # make sure the file has a filename
    if file.filename == '':
        return render_template('error.html', error='File does not have a filename')

    if not allowed_file(file.filename):
        return render_template('error.html',
                               error=f'file extension of "{file.filename}" not allowed')

    # success!
    filename = secure_filename(file.filename)
    file.save(os.path.join(App.config['UPLOAD_FOLDER'], filename)) # TODO replace with Azure!!
    return f'{filename} uploaded successfully'


if __name__ == "__main__":
    App.run()
