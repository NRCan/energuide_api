from http import HTTPStatus
import pymongo
import pytest
from flask import testing
from energuide import flask_app
from energuide import database


flask_app.App.testing = True


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


def test_trigger_tl(test_client: testing.FlaskClient,
                    energuide_zip_fixture: str,
                    mongo_client: pymongo.MongoClient,
                    database_name: str,
                    collection: str) -> None:

    post_return = test_client.post('/trigger_tl', data=dict(filename=energuide_zip_fixture))
    assert post_return.status_code == HTTPStatus.CREATED
    assert mongo_client[database_name][collection].count() == 7
