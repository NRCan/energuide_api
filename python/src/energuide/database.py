from contextlib import contextmanager
import enum
import typing

import os
import pymongo
import pandas as pd


class EnvVariables(enum.Enum):
    username = 'ENERGUIDE_USERNAME'
    password = 'ENERGUIDE_PASSWORD'
    host = 'ENERGUIDE_HOST'
    port = 'ENERGUIDE_PORT'
    database = 'ENERGUIDE_DBNAME'
    collection = 'ENERGUIDE_COLLECTION'


class EnvDefaults(enum.Enum):
    username = ''
    password = ''
    host = 'localhost'
    port = 27017
    database = 'energuide'
    collection = 'dwellings'


class DatabaseCoordinates(typing.NamedTuple):
    username: str
    password: str
    host: str
    port: int
    database: str
    collection: str


def _is_prod() -> bool:
    return bool(os.environ.get('PROD'))


def _build_connection_string(coords: DatabaseCoordinates) -> str:
    username, password, host, port, _, _ = coords

    if _is_prod():
        connection_string = f'mongodb+srv://{username}:{password}@{host}'
    else:
        prefix = f'{username}:{password}@' if username and password else ''
        connection_string = f'{prefix}{host}:{port}'

    return connection_string


@contextmanager  # type: ignore
def mongo_client(database_coordinates: DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    connection_string = _build_connection_string(database_coordinates)
    with pymongo.MongoClient(f'{connection_string}') as client:
        yield client


def load(coords: DatabaseCoordinates,
         dataframe: pd.DataFrame) -> None:
    database_name = coords.database
    collection_name = coords.collection

    client: pymongo.MongoClient
    with mongo_client(coords) as client:
        database = client[database_name]
        collection = database[collection_name]

        collection.insert_many(dataframe.to_dict('records'))
