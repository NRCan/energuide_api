import os

import pymongo
import pytest
from energuide import database


@pytest.fixture
def energuide_data() -> str:
    return os.path.join(os.path.dirname(__file__), 'sample.csv')


def test_load_all(database_coordinates: database.DatabaseCoordinates,
                  mongo_client: pymongo.MongoClient,
                  energuide_data: str) -> None:

    database_name = database_coordinates.database
    collection_name = database_coordinates.collection

    mongo_client[database_name][collection_name].drop()
    database.load(database_coordinates, energuide_data)

    assert mongo_client[database_name][collection_name].count() == 2001
