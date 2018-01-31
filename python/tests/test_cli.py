import zipfile
import py
import _pytest
from click import testing  # type: ignore
import pymongo
import pytest
from energuide import cli


@pytest.fixture(params=[
    '''EVAL_ID,EVAL_TYPE,ENTRYBY,CLIENTADDR,CLIENTPCODE,CLIENTNAME,TELEPHONE,MAIL_ADDR,\
MAIL_PCODE,TAXNUMBER,RAW_XML,BUILDER\n123,D,Fred Johnson,123 Main st.,M5E 1W5,John \
Fredson,999 999 9999,123 Main st.,M5E 1W5,999999999999,<tag>thing</tag>,4K13D01404''',
    '''EVAL_ID,EVAL_TYPE,ENTRYBY,CLIENTADDR,CLIENTPCODE,CLIENTNAME,TELEPHONE,MAIL_ADDR,\
MAIL_PCODE,TAXNUMBER,RAW_XML,BUILDER,other_1,other_2\n123,D,Fred Johnson,123 Main st.,M5E 1W5,John \
Fredson,999 999 9999,123 Main st.,M5E 1W5,999999999999,<tag>thing</tag>,4K02E90020,foo,bar'''])
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
        file.write('EVAL_ID,EVAL_TYPE,BUILDER\nfoo,bar,\nfoo,bar,4K02E90020')

    return filepath


def test_load(energuide_zip_fixture: str,
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
