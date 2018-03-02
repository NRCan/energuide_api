from http import HTTPStatus
import hashlib
import typing
import pymongo
import pytest
from flask import testing
from energuide import flask_app
from energuide import database


flask_app.App.testing = True


@pytest.fixture
def sample_salt() -> str:
    return 'sample salt'


@pytest.fixture
def sample_secret_key() -> typing.Generator:
    orig_secret_key = flask_app.App.config['SECRET_KEY']
    flask_app.App.config['SECRET_KEY'] = 'sample secret key'

    yield flask_app.App.config['SECRET_KEY']

    flask_app.App.config['SECRET_KEY'] = orig_secret_key


@pytest.fixture
def sample_signature(sample_salt: str, sample_secret_key: str) -> str:
    return hashlib.sha3_256((sample_salt + sample_secret_key).encode()).hexdigest()


@pytest.fixture()
def test_client(database_coordinates: database.DatabaseCoordinates,
                database_name: str,
                collection: str) -> testing.FlaskClient:
    orig_database_coords = flask_app.DATABASE_COORDS
    orig_database_name = flask_app.DATABASE_NAME
    orig_collection = flask_app.COLLECTION
    flask_app.DATABASE_COORDS = database_coordinates
    flask_app.DATABASE_NAME = database_name
    flask_app.COLLECTION = collection

    yield flask_app.App.test_client()

    flask_app.DATABASE_COORDS = orig_database_coords
    flask_app.DATABASE_NAME = orig_database_name
    flask_app.COLLECTION = orig_collection


def test_frontend(test_client: testing.FlaskClient) -> None:
    assert test_client.get('/').status_code == HTTPStatus.OK


def test_alive(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/test_alive')
    assert b'Alive' in get_return.data


def test_robots(test_client: testing.FlaskClient) -> None:
    get_return = test_client.get('/robots933456.txt')
    assert get_return.status_code == HTTPStatus.NOT_FOUND


def test_trigger_tl(test_client: testing.FlaskClient,
                    energuide_zip_fixture: str,
                    mongo_client: pymongo.MongoClient,
                    database_name: str,
                    collection: str,
                    sample_salt: str,
                    sample_signature: str) -> None:

    post_return = test_client.post('/trigger_tl',
                                   data=dict(filename=energuide_zip_fixture,
                                             salt=sample_salt,
                                             signature=sample_signature))
    assert post_return.status_code == HTTPStatus.CREATED
    assert mongo_client[database_name][collection].count() == 7


def test_trigger_no_salt(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_signature: str) -> None:
    post_return = test_client.post('/trigger_tl',
                                   data=dict(filename=energuide_zip_fixture,
                                             signature=sample_signature))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'no salt' in post_return.data


def test_trigger_no_signature(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_salt: str) -> None:
    post_return = test_client.post('/trigger_tl', data=dict(filename=energuide_zip_fixture, salt=sample_salt))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'no signature' in post_return.data


def test_trigger_bad_signature(test_client: testing.FlaskClient, energuide_zip_fixture: str, sample_salt: str) -> None:
    post_return = test_client.post('/trigger_tl',
                                   data=dict(filename=energuide_zip_fixture,
                                             salt=sample_salt,
                                             signature='bad signature'))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'bad signature' in post_return.data


def test_trigger_no_filename(test_client: testing.FlaskClient, sample_salt: str, sample_signature: str) -> None:
    post_return = test_client.post('/trigger_tl', data=dict(salt=sample_salt, signature=sample_signature))
    assert post_return.status_code == HTTPStatus.BAD_REQUEST
    assert b'no filename' in post_return.data
