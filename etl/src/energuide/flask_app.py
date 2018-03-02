import os
import typing
from http import HTTPStatus
import hashlib
import flask
import pymongo
from energuide import transform
from energuide import database


App = flask.Flask(__name__)


DEFAULT_ETL_SECRET_KEY = 'no key'

App.config.update(dict(
    SECRET_KEY=os.environ.get('ETL_SECRET_KEY', DEFAULT_ETL_SECRET_KEY),
))


DATABASE_COORDS = database.DatabaseCoordinates(
    username=os.environ.get(database.EnvVariables.username.value, default=database.EnvDefaults.username.value),
    password=os.environ.get(database.EnvVariables.password.value, default=database.EnvDefaults.password.value),
    host=os.environ.get(database.EnvVariables.host.value, default=database.EnvDefaults.host.value),
    port=int(os.environ.get(database.EnvVariables.port.value, default=database.EnvDefaults.port.value))
)

DATABASE_NAME = os.environ.get(database.EnvVariables.database.value, default=database.EnvDefaults.database.value)

COLLECTION = os.environ.get(database.EnvVariables.collection.value, default=database.EnvDefaults.collection.value)


def trigger(filename: str,
            coords: database.DatabaseCoordinates,
            database_name: str,
            collection: str) -> typing.Tuple[str, int]:

    transform.run(coords,
                  database_name=database_name,
                  collection=collection,
                  filename=filename,
                  append=False)

    mongo_client: pymongo.MongoClient
    with database.mongo_client(coords) as mongo_client:
        records_created = mongo_client[database_name][collection].count()
    return f'success, {records_created} created', HTTPStatus.CREATED


@App.route('/', methods=['GET'])
def frontend() -> str:
    return ''


@App.route('/test_alive', methods=['GET'])
def test_alive() -> str:
    return 'Alive!'


@App.route('/robots933456.txt', methods=['GET'])
def robots() -> None:
    flask.abort(HTTPStatus.NOT_FOUND)


@App.route('/trigger_tl_get', methods=['GET'])
def trigger_tl_get() -> typing.Tuple[str, int]:
    return trigger('extract_out.zip', DATABASE_COORDS, DATABASE_NAME, COLLECTION)


@App.route('/trigger_tl', methods=['POST'])
def trigger_tl() -> typing.Tuple[str, int]:
    if 'filename' not in flask.request.form:
        return 'no filename', HTTPStatus.BAD_REQUEST
    if 'salt' not in flask.request.form:
        return 'no salt', HTTPStatus.BAD_REQUEST
    if 'signature' not in flask.request.form:
        return 'no signature', HTTPStatus.BAD_REQUEST

    filename = flask.request.form['filename']
    salt = flask.request.form['salt']
    signature = flask.request.form['signature']

    salt_signature = hashlib.sha256((salt + App.config['SECRET_KEY']).encode()).hexdigest()
    if salt_signature != signature:
        return 'bad signature', HTTPStatus.BAD_REQUEST

    return trigger(filename, DATABASE_COORDS, DATABASE_NAME, COLLECTION)


if __name__ == "__main__":
    App.run(host='0.0.0.0')
