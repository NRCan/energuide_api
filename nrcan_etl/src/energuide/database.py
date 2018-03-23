from contextlib import contextmanager
import enum
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
        for row in data:
            num_rows += 1
            data_row = row.to_dict()
            collection.update({'houseId': data_row['houseId']}, data_row, upsert=True)
        LOGGER.info(f"updated {num_rows} rows in the database")
