import csv
import os
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
        'HOUSE_ID': '456',
        'EVAL_TYPE': 'D',
        'BUILDER': '4K13D01404',
        'ENTRYDATE': '2012-02-25',
        'CREATIONDATE': '2012-06-08 09:26:10',
        'MODIFICATIONDATE': '2012-06-09 09:26:10',
        'YEARBUILT': '1894',
        'CLIENTCITY': 'Brooks',
        'HOUSEREGION': 'AB',
        'MAIL_PCODE': 'L1R5C7',
        'HEATEDFLOORAREA': '201.1351',
        'TYPEOFHOUSE': 'Single detached',
        'ERSRATING': '164',
        'UGRERSRATING': '115',
        'ERSGHG': '7.8',
        'UGRERSGHG': '5.4',
        'ERSENERGYINTENSITY': '0.82',
        'UGRERSENERGYINTENSITY': '0.80',
        'EGHDESHTLOSS': '11242.1',
        'UGRDESHTLOSS': '10757.3',
        'EGHRATING': '50',
        'UGRRATING': '49',

        'WALLDEF': '45.3;12;50;12;4.7;12',
        'UGRWALLDEF': '45.3;12;50;12;4.7;10',
        'EGHHLWALLS': '27799.9',
        'UGRHLWALLS': '27799.9',

        'RAW_XML': '',
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
    filepath = os.path.join(tmpdir, 'sample.csv')

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
    assert coll.count() == 11


@pytest.mark.usefixtures('populated_azure_emulator')
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
    assert coll.count() == 11


def test_load_update(energuide_zip_fixture: str,
                     database_name: str,
                     collection: str,
                     mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_zip_fixture,
        '--no-update',
    ])

    assert result.exit_code == 0

    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_zip_fixture,
        '--update',
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 11


def test_extract_valid(valid_filepath: str, tmpdir: py._path.local.LocalPath) -> None:
    outfile = os.path.join(tmpdir, 'output.zip')
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

    assert result.exit_code == 0

    with zipfile.ZipFile(outfile, 'r') as output:
        assert not output.namelist()


def test_extract_missing(tmpdir: py._path.local.LocalPath) -> None:
    outfile = os.path.join(tmpdir, 'output.zip')
    infile = os.path.join(tmpdir, 'idontexist.csv')
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', infile,
        '--outfile', outfile
    ])

    assert result.exit_code != 0
    assert not os.path.exists(outfile)
