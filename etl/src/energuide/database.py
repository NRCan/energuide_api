from contextlib import contextmanager
import enum
import typing

import pymongo

from energuide import dwelling


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
    with pymongo.MongoClient(f'{database_coordinates.connection_string}') as client:
        yield client


_DEFAULT_CHUNK_SIZE = 1000


def _chunk_data(data: typing.Iterable[dwelling.Dwelling],
                max_chunk_size: int = _DEFAULT_CHUNK_SIZE
               ) -> typing.Iterator[typing.List[typing.Dict[str, typing.Any]]]:

    chunked_list: typing.List[typing.Dict[str, typing.Any]] = []
    load_size = 0

    for row in data:
        if load_size >= max_chunk_size:
            yield chunked_list
            chunked_list = []
            load_size = 0
        chunked_list.append(row.to_dict())
        load_size += 1

    if chunked_list:
        yield chunked_list


def load(coords: DatabaseCoordinates,
         database_name: str,
         collection_name: str,
         data: typing.Iterable[dwelling.Dwelling],
         append: bool = False) -> None:

    client: pymongo.MongoClient
    with mongo_client(coords) as client:
        database = client[database_name]
        collection = database[collection_name]

        if not append:
            collection.drop()

        for data_to_load in _chunk_data(data):
            collection.insert_many(data_to_load)
