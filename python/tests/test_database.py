import typing
import pymongo
import pytest
from energuide import database
from energuide import dwelling


@pytest.fixture
def load_data() -> typing.List[dwelling.Dwelling]:
    return [
        dwelling.Dwelling(house_id=1, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          postal_code='K1P 0A6', forward_sortation_area='K1P', evaluations=[]),
        dwelling.Dwelling(house_id=1, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          postal_code='K1P 0A6', forward_sortation_area='K1P', evaluations=[]),
        dwelling.Dwelling(house_id=1, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          postal_code='K1P 0A6', forward_sortation_area='K1P', evaluations=[]),
    ]


def test_load(database_coordinates: database.DatabaseCoordinates,
                      mongo_client: pymongo.MongoClient,
                      database_name: str,
                      collection: str,
                      load_data: typing.List[dwelling.Dwelling]):
    database.load(database_coordinates, database_name, collection, load_data)
    assert mongo_client[database_name][collection].count() == 3
