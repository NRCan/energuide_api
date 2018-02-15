import _pytest
import pymongo
from energuide import database
from energuide import transform
from energuide.embedded import ceiling
from energuide.exceptions import InvalidEmbeddedDataTypeException


def test_run(database_coordinates: database.DatabaseCoordinates,
             mongo_client: pymongo.MongoClient,
             database_name: str,
             collection: str,
             energuide_zip_fixture: str) -> None:

    stats = transform.run(database_coordinates, database_name, collection, energuide_zip_fixture)
    assert mongo_client[database_name][collection].count() == 7
    assert stats.success == stats.total == 7


def test_bad_run(database_coordinates: database.DatabaseCoordinates,
                 mongo_client: pymongo.MongoClient,
                 database_name: str,
                 collection: str,
                 energuide_zip_fixture: str,
                 monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:

    def raise_exception(*args): # pylint: disable=unused-argument
        raise InvalidEmbeddedDataTypeException(ceiling.Ceiling)

    monkeypatch.setattr(ceiling.Ceiling, 'from_data', raise_exception)
    stats = transform.run(database_coordinates, database_name, collection, energuide_zip_fixture)

    assert mongo_client[database_name][collection].count() == 0
    assert stats.total == stats.failure == 7
