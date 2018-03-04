import os
import random
import socket
import typing
import zipfile
import py
import _pytest.monkeypatch
import pymongo
import pytest
from azure.storage import blob
from energuide import database
from energuide import extractor


def azure_emulator_is_running() -> bool:
    if 'CIRCLECI' in os.environ:
        return True

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 10000))
    except socket.error:
        return True
    else:
        sock.close()
        return False


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
def azure_container_name() -> str:
    return 'test-container'


@pytest.fixture
def azure_service(azure_container_name: str,
                  monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> typing.Iterator[blob.BlockBlobService]:
    if not azure_emulator_is_running():
        pytest.skip("Azure emulator is not running.")

    account = 'devstoreaccount1'
    key = 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    domain = 'http://127.0.0.1:10000/devstoreaccount1'
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', account)
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_KEY', key)
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_DOMAIN', domain)
    monkeypatch.setenv('EXTRACT_ENDPOINT_CONTAINER', azure_container_name)

    azure_service = blob.BlockBlobService(account_name=account,
                                          account_key=key,
                                          custom_domain=domain)
    azure_service.create_container(azure_container_name)
    yield azure_service
    azure_service.delete_container(azure_container_name)


@pytest.fixture
def populated_azure_service(azure_service: blob.BlockBlobService,
                            azure_container_name: str,
                            energuide_zip_fixture: str) -> blob.BlockBlobService:

    file_z = zipfile.ZipFile(energuide_zip_fixture)
    azure_service.create_blob_from_text(azure_container_name, 'timestamp.txt', 'Wednesday')
    for json_file in [file_z.open(zipinfo) for zipinfo in file_z.infolist()]:
        azure_service.create_blob_from_bytes(azure_container_name, json_file.name, json_file.read())

    return azure_service
