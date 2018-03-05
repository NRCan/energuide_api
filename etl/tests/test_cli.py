import csv
import typing
import zipfile
import py
import _pytest
from click import testing  # type: ignore
import pymongo
import pytest
from energuide import cli


def data1() -> typing.Dict[str, typing.Optional[str]]:
    return {
        'EVAL_ID': '123',
        'EVAL_TYPE': 'D',
        'ENTRYBY': 'Fred Johnson',
        'CLIENTADDR': '123 Main st.',
        'CLIENTPCODE': 'M5E 1W5',
        'CLIENTNAME': 'John Fredson',
        'TELEPHONE': '999 999 9999',
        'MAIL_ADDR': '123 Main st.',
        'MAIL_PCODE': 'M5E 1W5',
        'TAXNUMBER': '999999999999',
        'RAW_XML': '<tag>thing</tag>',
        'BUILDER': '4K13D01404',
        'DHWHPCOP': '0',
        'ERSRATING': '200',
        'INFO1': None,
        'INFO2': None,
        'INFO3': None,
        'INFO4': None,
        'INFO5': None,
        'INFO6': None,
        'INFO7': None,
        'INFO8': None,
        'INFO9': None,
        'INFO10': None,
        'ENTRYDATE': '2012-02-25',
        'CREATIONDATE': '2012-06-08 09:26:10',
        'MODIFICATIONDATE': '2012-06-09 09:26:10',
        'YEARBUILT': '1894',
        'CLIENTCITY': 'Brooks',
        'HOUSEREGION': 'AB',
    }


def data2() -> typing.Dict[str, typing.Optional[str]]:
    data = data1()
    data['other_1'] = 'foo'
    data['other_2'] = 'bar'
    return data


@pytest.fixture(params=[data1(), data2()])
def data_dict(request: _pytest.fixtures.SubRequest) -> typing.Dict[str, str]:
    return request.param


@pytest.fixture
def valid_filepath(tmpdir: py._path.local.LocalPath, data_dict: typing.Dict[str, str]) -> str:
    filepath = f'{tmpdir}/sample.csv'
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data_dict.keys()))
        writer.writeheader()
        writer.writerow(data_dict)

    return filepath


@pytest.fixture
def invalid_filepath(tmpdir: py._path.local.LocalPath) -> str:
    filepath = f'{tmpdir}/sample.csv'
    data = {'EVAL_ID': 'foo', 'EVAL_TYPE': 'bar'}
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)

    return filepath


def test_load_filename(energuide_zip_fixture: str,
                       database_name: str,
                       collection: str,
                       mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_zip_fixture,
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 7


@pytest.mark.usefixtures('populated_azure_service')
def test_load_azure(database_name: str,
                    collection: str,
                    mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--azure',
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 7


def test_load_append(energuide_zip_fixture: str,
                     database_name: str,
                     collection: str,
                     mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_zip_fixture,
    ])

    assert result.exit_code == 0

    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_zip_fixture,
        '--append',
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 14


def test_extract_valid(valid_filepath: str, tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.zip'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', valid_filepath,
        '--outfile', outfile
    ])

    assert result.exit_code == 0

    with zipfile.ZipFile(outfile, 'r') as output:
        assert len(output.namelist()) == 1


def test_extract_invalid(invalid_filepath: str, tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.zip'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', invalid_filepath,
        '--outfile', outfile
    ])

    assert result.exit_code != 0

    with zipfile.ZipFile(outfile, 'r') as output:
        assert not output.namelist()


def test_extract_missing(tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.zip'
    infile = f'{tmpdir}/idontexist.csv'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', infile,
        '--outfile', outfile
    ])

    assert result.exit_code != 0

    with zipfile.ZipFile(outfile, 'r') as output:
        assert not output.namelist()
