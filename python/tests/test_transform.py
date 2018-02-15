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
