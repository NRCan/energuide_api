import os
import py
import random
import typing
import pymongo
import pytest
from energuide import database
from energuide import extractor


@pytest.fixture
def username() -> str:
    return os.environ.get(database.EnvVariables.username.value, database.EnvDefaults.username.value)


@pytest.fixture
def password() -> str:
    return os.environ.get(database.EnvVariables.password.value, database.EnvDefaults.password.value)


@pytest.fixture
def host() -> str:
    return os.environ.get(database.EnvVariables.host.value, database.EnvDefaults.host.value)


@pytest.fixture
def port() -> int:
    return int(os.environ.get(database.EnvVariables.port.value, database.EnvDefaults.port.value))


@pytest.fixture
def production() -> bool:
    return bool(os.environ.get(database.EnvVariables.production.value, database.EnvDefaults.production.value))


@pytest.fixture
def database_name(database_coordinates: database.DatabaseCoordinates) -> typing.Iterable[str]:
    db_name = os.environ.get(database.EnvVariables.database.value, database.EnvDefaults.database.value)
    db_name = f'{db_name}_test_{random.randint(1000, 9999)}'

    yield db_name

    client: pymongo.MongoClient
    with database.mongo_client(database_coordinates) as client:
        client.drop_database(db_name)


@pytest.fixture
def collection() -> str:
    return os.environ.get(database.EnvVariables.collection.value, database.EnvDefaults.collection.value)


@pytest.fixture
def database_coordinates(username: str,
                         password: str,
                         host: str,
                         port: int,
                         production: bool) -> database.DatabaseCoordinates:
    return database.DatabaseCoordinates(
        username=username,
        password=password,
        host=host,
        port=port,
        production=production,
    )


@pytest.fixture
def mongo_client(database_coordinates: database.DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    client: pymongo.MongoClient
    with database.mongo_client(database_coordinates) as client:
        yield client

@pytest.fixture
def energuide_fixture() -> str:
    return os.path.join(os.path.dirname(__file__), 'scrubbed_random_sample_xml.csv')


@pytest.fixture
def energuide_zip_fixture(tmpdir: py._path.local.LocalPath, energuide_fixture: str) -> str:
    outfile = os.path.join(tmpdir, 'scrubbed_random_sample_xml.zip')

    data = extractor.extract_data(energuide_fixture)
    extractor.write_data(data, outfile)
    return outfile
