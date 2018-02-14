import pymongo
from energuide import database
from energuide import transform


def test_run(database_coordinates: database.DatabaseCoordinates,
             mongo_client: pymongo.MongoClient,
             database_name: str,
             collection: str,
             energuide_zip_fixture: str) -> None:

    stats = transform.run(database_coordinates, database_name, collection, energuide_zip_fixture)
    assert mongo_client[database_name][collection].count() == 7
    assert stats.success == stats.total == 7


def test_run_bad_data(database_coordinates: database.DatabaseCoordinates,
                      mongo_client: pymongo.MongoClient,
                      database_name: str,
                      collection: str,
                      energuide_bad_zip_fixture: str) -> None:

    stats = transform.run(database_coordinates, database_name, collection, energuide_bad_zip_fixture)
    assert mongo_client[database_name][collection].count() == 6
    assert stats.success == 6
    assert stats.failure == 2
