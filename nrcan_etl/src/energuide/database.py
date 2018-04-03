from contextlib import contextmanager
import enum
from itertools import islice
import typing

import pymongo

from energuide import dwelling
from energuide import logger


LOGGER = logger.get_logger(__name__)


class EnvVariables(enum.Enum):
    username = 'ENERGUIDE_USERNAME'
    password = 'ENERGUIDE_PASSWORD'
    host = 'ENERGUIDE_HOST'
    port = 'ENERGUIDE_PORT'
    database = 'ENERGUIDE_DBNAME'
    collection = 'ENERGUIDE_COLLECTION'
    production = 'ENERGUIDE_PRODUCTION'


class EnvDefaults(enum.Enum):
    username = ''
    password = ''
    host = 'localhost'
    port = 27017
    database = 'energuide'
    collection = 'dwellings'
    production = False


class _DatabaseCoordinates(typing.NamedTuple):
    username: str
    password: str
    host: str
    port: int
    production: bool = False


class DatabaseCoordinates(_DatabaseCoordinates):
    @property
    def connection_string(self) -> str:
        if self.production:
            connection_string = f'mongodb+srv://{self.username}:{self.password}@{self.host}'
        else:
            prefix = f'{self.username}:{self.password}@' if self.username and self.password else ''
            connection_string = f'{prefix}{self.host}:{self.port}'
        return connection_string


@contextmanager  # type: ignore
def mongo_client(database_coordinates: DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    connection_string = database_coordinates.connection_string

    LOGGER.info(
        f'Connecting to {database_coordinates.host}, using method '
        f"{['local', 'production'][database_coordinates.production]}"
    )

    with pymongo.MongoClient(f'{connection_string}') as client:
        yield client


CHUNKSIZE = 1000

T = typing.TypeVar('T')
def _chunk(data: typing.Iterable[T], size=CHUNKSIZE) -> typing.Iterable[typing.List[T]]:
    iterator = iter(data)
    chunk = list(islice(iterator, size))

    while len(chunk) == size:
        yield chunk
        chunk = list(islice(iterator, size))

    if not chunk:
        return
    else:
        yield chunk


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

        num_rows = 0
        request = lambda document: pymongo.ReplaceOne({'houseId': document['houseId']}, document, upsert=True)

        for chunk in _chunk(data):
            num_rows += len(chunk)
            requests = [request(document.to_dict()) for document in chunk]
            collection.bulk_write(requests, ordered=False)

        LOGGER.info(f"updated {num_rows} rows in the database")
