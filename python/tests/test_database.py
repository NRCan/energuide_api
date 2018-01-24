import pandas as pd
import pymongo
import pytest
from energuide import database


@pytest.fixture
def energuide_data(energuide_fixture: str) -> pd.DataFrame:
    return pd.read_csv(energuide_fixture)


def test_load_all(database_coordinates: database.DatabaseCoordinates,
                  mongo_client: pymongo.MongoClient,
                  database_name: str,
                  collection: str,
                  energuide_data: pd.DataFrame) -> None:

    database.load(database_coordinates, database_name, collection, energuide_data)

    assert mongo_client[database_name][collection].count() == 3
