import os
import typing

import pymongo
import pytest
from energuide import database

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
def database_name():
    return os.environ.get(database.EnvVariables.database.value, database.EnvDefaults.database.value)

@pytest.fixture
def collection() -> str:
    return os.environ.get(database.EnvVariables.collection.value, database.EnvDefaults.collection.value)

@pytest.fixture
def database_coordinates(username: str,
                         password: str,
                         host: str,
                         port: int,
                         database_name: str,
                         collection: str) -> database.DatabaseCoordinates:
    return database.DatabaseCoordinates(
               username=username,
               password=password,
               host=host,
               port=port,
               database=database_name,
               collection=collection
           )

@pytest.fixture
def mongo_client(database_coordinates: database.DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    connection_string = database.build_connection_string(database_coordinates)
    with pymongo.MongoClient(f'{connection_string}') as client:
        yield client
