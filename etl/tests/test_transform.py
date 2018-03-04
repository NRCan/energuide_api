import _pytest
import pytest
import pymongo
from energuide import database
from energuide import transform
from energuide.embedded import ceiling
from energuide.exceptions import InvalidEmbeddedDataTypeError


def test_run_no_azure(database_coordinates: database.DatabaseCoordinates,
                      mongo_client: pymongo.MongoClient,
                      database_name: str,
                      collection: str,
                      energuide_zip_fixture: str) -> None:

    transform.run(database_coordinates, database_name, collection, False, energuide_zip_fixture, append=False)
    assert mongo_client[database_name][collection].count() == 7


@pytest.mark.usefixtures('populated_azure_service')
def test_run_azure(database_coordinates: database.DatabaseCoordinates,
                   mongo_client: pymongo.MongoClient,
                   database_name: str,
                   collection: str) -> None:

    transform.run(database_coordinates, database_name, collection, True, None, append=False)
    assert mongo_client[database_name][collection].count() == 7


def test_run_no_azure_no_filename(database_coordinates: database.DatabaseCoordinates,
                                  database_name: str,
                                  collection: str) -> None:
    with pytest.raises(ValueError):
        transform.run(database_coordinates, database_name, collection, False, None, append=False)


def test_bad_data(database_coordinates: database.DatabaseCoordinates,
                  mongo_client: pymongo.MongoClient,
                  database_name: str,
                  collection: str,
                  energuide_zip_fixture: str,
                  monkeypatch: _pytest.monkeypatch.MonkeyPatch,
                  capsys: _pytest.capture.CaptureFixture) -> None:

    def raise_error(*args) -> None: #pylint: disable=unused-argument
        raise InvalidEmbeddedDataTypeError(ceiling.Ceiling)

    monkeypatch.setattr(ceiling.Ceiling, 'from_data', raise_error)

    transform.run(database_coordinates, database_name, collection, False, energuide_zip_fixture, append=False)
    assert mongo_client[database_name][collection].count() == 0

    _, err = capsys.readouterr()
    assert all('Ceiling' in line for line in err.split()[1:-1])
