import io
import datetime
import zipfile
import typing
import pytest
import py
from azure.storage import blob
from extract_endpoint import azure_utils, endpoint


@pytest.fixture(scope='session')
def azure_emulator_coords() -> azure_utils.StorageCoordinates:
    return azure_utils.StorageCoordinates(
        account='devstoreaccount1',
        key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
        container='test-container',
        domain='http://127.0.0.1:10000/devstoreaccount1',
    )


@pytest.fixture
def azure_service(azure_emulator_coords) -> blob.BlockBlobService:
    azure_service = blob.BlockBlobService(account_name=azure_emulator_coords.account,
                                          account_key=azure_emulator_coords.key,
                                          custom_domain=azure_emulator_coords.domain)
    azure_service.create_container(azure_emulator_coords.container)
    yield azure_service
    azure_service.delete_container(azure_emulator_coords.container)


@pytest.fixture
def sample_timestamp() -> str:
    return datetime.datetime(2018, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def sample_filenames() -> typing.Tuple[str, str]:
    return ("sample_filename_1.txt", "sample_filename_2.txt")


@pytest.fixture
def sample_file_contents() -> typing.Tuple[str, str]:
    return ("sample file contents 1", "sample file contents 2")


@pytest.fixture
def sample_zipfile(sample_filenames: typing.Tuple[str, str],
                   sample_file_contents: typing.Tuple[str, str]) -> io.BytesIO:

    file = io.BytesIO()
    file_z = zipfile.ZipFile(file, 'w')
    for name, contents in zip(sample_filenames, sample_file_contents):
        file_z.writestr(name, contents)
    file_z.close()
    file.seek(0)
    return file


@pytest.fixture
def sample_secret_key(monkeypatch) -> str:
    monkeypatch.setitem(endpoint.App.config, 'SECRET_KEY', 'sample secret key')
    return endpoint.App.config['SECRET_KEY']


@pytest.fixture
def sample_zipfile_fixture(tmpdir: py._path.local.LocalPath,
                           sample_filenames: typing.Tuple[str, str],
                           sample_file_contents: typing.Tuple[str, str]) -> str:
    file = f'{tmpdir}/sample_zipfile.zip'
    file_z = zipfile.ZipFile(file, 'w')
    for name, contents in zip(sample_filenames, sample_file_contents):
        file_z.writestr(name, contents)
    file_z.close()
    return file
