from click import testing  # type: ignore
import pymongo
from energuide import cli


def test_load(energuide_fixture: str, database_name: str, collection: str, mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_fixture,
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 3
