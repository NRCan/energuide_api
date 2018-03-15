from contextlib import contextmanager
import enum
import typing

import os
import pymongo

from energuide import dwelling


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


def _is_prod() -> bool:
    return bool(os.environ.get('PROD'))


def _build_connection_string(coords: DatabaseCoordinates) -> str:
    username, password, host, port = coords

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
         database_name: str,
         collection_name: str,
         data: typing.Iterable[dwelling.Dwelling],
         update: bool = True) -> None:
    client: pymongo.MongoClient
    with mongo_client(coords) as client:
        database = client[database_name]
        collection = database[collection_name]

        if not update:
            collection.drop()

        existing = set(collection.distinct('houseId'))

        for row in data:
            existing.discard(row.house_id)
            data_row = row.to_dict()
            collection.update({'houseId': data_row['houseId']}, data_row, upsert=True)

        collection.remove({'houseId': {'$in': list(existing)}})
