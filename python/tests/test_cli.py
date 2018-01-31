import os
import py
import _pytest
from click import testing  # type: ignore
import pymongo
import pytest
from energuide import cli


@pytest.fixture(params=[
    '''EVAL_ID,EVAL_TYPE,ENTRYBY,CLIENTADDR,CLIENTPCODE,CLIENTNAME,TELEPHONE,MAIL_ADDR,\
MAIL_PCODE,TAXNUMBER,RAW_XML\n123,D,Fred Johnson,123 Main st.,M5E 1W5,John \
Fredson,999 999 9999,123 Main st.,M5E 1W5,999999999999,<tag>thing</tag>''',
    '''EVAL_ID,EVAL_TYPE,ENTRYBY,CLIENTADDR,CLIENTPCODE,CLIENTNAME,TELEPHONE,MAIL_ADDR,\
MAIL_PCODE,TAXNUMBER,RAW_XML,other_1,other_2\n123,D,Fred Johnson,123 Main st.,M5E 1W5,John \
Fredson,999 999 9999,123 Main st.,M5E 1W5,999999999999,<tag>thing</tag>,foo,bar'''])
def passing_str(request: _pytest.fixtures.SubRequest) -> str:
    return request.param


@pytest.fixture
def valid_filepath(tmpdir: py._path.local.LocalPath, passing_str: str) -> str:
    filepath = f'{tmpdir}/sample.csv'
    with open(filepath, 'w') as file:
        file.write(passing_str)

    return filepath


@pytest.fixture
def invalid_filepath(tmpdir: py._path.local.LocalPath) -> str:
    filepath = f'{tmpdir}/sample.csv'
    with open(filepath, 'w') as file:
        file.write('EVAL_ID,EVAL_TYPE\nfoo,bar')

    return filepath


def test_load(energuide_fixture: str, database_name: str, collection: str, mongo_client: pymongo.MongoClient) -> None:
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'load',
        '--db_name', database_name,
        '--filename', energuide_fixture,
    ])

    assert result.exit_code == 0

    coll = mongo_client.get_database(database_name).get_collection(collection)
    assert coll.count() == 7


def test_extract_valid(valid_filepath: str, tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.json'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', valid_filepath,
        '--outfile', outfile
    ])

    assert result.exit_code == 0
    assert os.path.isfile(outfile)


def test_extract_invalid(invalid_filepath: str, tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.json'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', invalid_filepath,
        '--outfile', outfile
    ])

    assert result.exit_code != 0
    assert not os.path.isfile(outfile)


def test_extract_empty(tmpdir: py._path.local.LocalPath) -> None:
    outfile = f'{tmpdir}/output.json'
    infile = f'{tmpdir}/idontexist.csv'
    runner = testing.CliRunner()
    result = runner.invoke(cli.main, args=[
        'extract',
        '--infile', infile,
        '--outfile', outfile
    ])

    assert result.exit_code != 0 
    assert not os.path.isfile(outfile)



