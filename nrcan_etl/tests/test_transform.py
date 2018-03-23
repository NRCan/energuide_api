import time
import zipfile
import _pytest
import pytest
from azure.storage import blob
from energuide import transform


@pytest.fixture
def local_reader(energuide_zip_fixture: str) -> transform.LocalExtractReader:
    return transform.LocalExtractReader(energuide_zip_fixture)


@pytest.fixture
def azure_reader(populated_azure_emulator: transform.AzureCoordinates) -> transform.AzureExtractReader:
    return transform.AzureExtractReader(populated_azure_emulator)


def test_reader(local_reader: transform.LocalExtractReader) -> None:
    output = list(local_reader.extracted_rows())
    output = sorted(output, key=lambda row: row['BUILDER'])
    unique_builders = {row['BUILDER'] for row in output}
    assert len(output) == 21
    assert output[0]['BUILDER'] == '1521D00144'
    assert len(unique_builders) == 21


def test_reader_num_rows(local_reader: transform.LocalExtractReader) -> None:
    assert local_reader.num_rows() == 21


def test_azure_reader_extracted_rows(azure_reader: transform.AzureExtractReader) -> None:
    output = list(azure_reader.extracted_rows())
    output = sorted(output, key=lambda row: row['BUILDER'])
    unique_builders = {row['BUILDER'] for row in output}
    assert len(output) == 21
    assert output[0]['BUILDER'] == '1521D00144'
    assert len(unique_builders) == 21


def touch_one_file_in_azure(azure_emulator: transform.AzureCoordinates, energuide_zip_fixture: str) -> None:
    file_z = zipfile.ZipFile(energuide_zip_fixture)
    service = blob.BlockBlobService(account_name=azure_emulator.account,
                                    account_key=azure_emulator.key,
                                    custom_domain=azure_emulator.domain)
    json_file = [file_z.open(zipinfo) for zipinfo in file_z.infolist()][1]
    service.create_blob_from_bytes(azure_emulator.container, json_file.name, json_file.read())


def test_azure_reader_extracted_rows_new_data(azure_reader: transform.AzureExtractReader,
                                              azure_emulator: transform.AzureCoordinates,
                                              energuide_zip_fixture: str) -> None:
    time.sleep(1)  # otherwise the files created in Azure will have the same modification time as timestamp_tl_start.txt
    output = list(azure_reader.extracted_rows())
    assert len(output) == 21

    azure_reader._new_file_list = None
    touch_one_file_in_azure(azure_emulator, energuide_zip_fixture)
    output = list(azure_reader.extracted_rows())
    assert len(output) == 2


def test_azure_reader_num_rows(azure_reader: transform.AzureExtractReader) -> None:
    assert azure_reader.num_rows() == 21


def test_azure_reader_num_rows_new_data(azure_reader: transform.AzureExtractReader) -> None:
    time.sleep(1)  # otherwise the files created in Azure will have the same modification time as timestamp_tl_start.txt
    azure_reader.num_rows()
    azure_reader._new_file_list = None
    assert azure_reader.num_rows() == 0


def test_azure_coordinates_from_env(monkeypatch: _pytest.monkeypatch.MonkeyPatch) -> None:
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', 'foo')
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_KEY', 'bar')
    monkeypatch.setenv('EXTRACT_ENDPOINT_STORAGE_DOMAIN', 'baz')
    monkeypatch.setenv('EXTRACT_ENDPOINT_CONTAINER', 'qux')
    coords = transform.AzureCoordinates.from_env()
    assert coords == transform.AzureCoordinates(
        account='foo',
        key='bar',
        domain='baz',
        container='qux'
    )


def test_transform(local_reader: transform.LocalExtractReader) -> None:
    output = transform.transform(local_reader)
    assert len(list(output)) == 11
