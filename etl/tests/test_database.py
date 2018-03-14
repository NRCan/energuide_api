import typing
import pymongo
import pytest
from energuide import database
from energuide import dwelling


@pytest.fixture
def load_data() -> typing.List[dwelling.Dwelling]:
    return [
        dwelling.Dwelling(house_id=1, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          forward_sortation_area='K1P', evaluations=[]),
        dwelling.Dwelling(house_id=2, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          forward_sortation_area='K1P', evaluations=[]),
        dwelling.Dwelling(house_id=3, year_built=2000, city='Ottawa', region=dwelling.Region.ONTARIO,
                          forward_sortation_area='K1P', evaluations=[]),
    ]


def test_load(database_coordinates: database.DatabaseCoordinates,
              mongo_client: pymongo.MongoClient,
              database_name: str,
              collection: str,
              load_data: typing.List[dwelling.Dwelling]):
    database.load(
        coords=database_coordinates,
        database_name=database_name,
        collection_name=collection,
        data=load_data,
        update=False
    )
    assert mongo_client[database_name][collection].count() == 3


def test_load_update(database_coordinates: database.DatabaseCoordinates,
                     mongo_client: pymongo.MongoClient,
                     database_name: str,
                     collection: str,
                     load_data: typing.List[dwelling.Dwelling]):
    database.load(
        coords=database_coordinates,
        database_name=database_name,
        collection_name=collection,
        data=load_data,
        update=False
    )
    assert mongo_client[database_name][collection].count() == 3
    load_data[0] = dwelling.Dwelling(house_id=1, year_built=2001, city='Ottawa', region=dwelling.Region.ONTARIO,
                                     forward_sortation_area='K1P', evaluations=[])
    load_data.append(
        dwelling.Dwelling(house_id=4, year_built=2001, city='Ottawa', region=dwelling.Region.ONTARIO,
                          forward_sortation_area='K1P', evaluations=[])
    )

    database.load(
        coords=database_coordinates,
        database_name=database_name,
        collection_name=collection,
        data=load_data,
        update=True
    )
    assert mongo_client[database_name][collection].count() == 4



