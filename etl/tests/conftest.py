import os
import random
import typing
import zipfile
import py
import pymongo
import pytest
from azure.storage import blob
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
                         port: int) -> database.DatabaseCoordinates:
    return database.DatabaseCoordinates(
        username=username,
        password=password,
        host=host,
        port=port,
    )


@pytest.fixture
def mongo_client(database_coordinates: database.DatabaseCoordinates) -> typing.Iterable[pymongo.MongoClient]:
    client: pymongo.MongoClient
    with database.mongo_client(database_coordinates) as client:
        yield client


@pytest.fixture
def energuide_fixture() -> str:
    return os.path.join(os.path.dirname(__file__), 'randomized_energuide_data.csv')


@pytest.fixture
def energuide_zip_fixture(tmpdir: py._path.local.LocalPath, energuide_fixture: str) -> str:
    outfile = f'{tmpdir}/randomized_energuide_data.zip'

    data = extractor.extract_data(energuide_fixture)
    extractor.write_data(data, outfile)
    return outfile


@pytest.fixture
def sample_fixture() -> str:
    return os.path.join(os.path.dirname(__file__), 'sample.csv')


@pytest.fixture
def azure_container() -> str:
    return 'test-container'


@pytest.fixture
def azure_service(azure_container: str) -> blob.BlockBlobService:
    azure_service = blob.BlockBlobService(account_name='devstoreaccount1',
                                          account_key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSR'
                                          + 'Z6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
                                          custom_domain='http://127.0.0.1:10000/devstoreaccount1')
    azure_service.create_container(azure_container)
    yield azure_service
    azure_service.delete_container(azure_container)


@pytest.fixture
def put_sample_files_in_azure(azure_service: blob.BlockBlobService,
                              azure_container: str,
                              energuide_zip_fixture: str) -> typing.Generator:

    file_z = zipfile.ZipFile(energuide_zip_fixture)
    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        azure_service.create_blob_from_text(azure_container, json_file.name, json_file.read())

    yield None

    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        azure_service.delete_blob(azure_container, json_file.name)
