import json
import typing
import zipfile
import _pytest
import py
import pytest
from energuide import extractor, reader


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
        file.write('EVAL_ID,EVAL_TYPE\nfoo,bar')

    return filepath


def test_extract_valid(valid_filepath: str) -> None:
    output = extractor.extract_data(valid_filepath)
    item = dict(next(output))

    assert 'EVAL_ID' in item

    assert 'CLIENTADDR' not in item


def test_extract_missing(invalid_filepath: str) -> None:
    with pytest.raises(reader.InvalidInputDataException) as ex:
        output = extractor.extract_data(invalid_filepath)
        _ = dict(next(output))

    assert 'EVAL_ID' not in ex.exconly()

    assert 'CLIENTADDR' in ex.exconly()


def test_write_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = f'{tmpdir}/output.zip'

    data = [
        {'foo': 1, 'BUILDER': '4K02E90020'},
        {'bar': 2, 'baz': 3, 'BUILDER': '4K13D01404'},
    ]

    extractor.write_data(data, output_path)

    with zipfile.ZipFile(output_path, 'r') as output_file:
        files = [output_file.read('4K02E90020'), output_file.read('4K13D01404')]

    assert [json.loads(file) for file in files] == data


def test_write_bad_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = f'{tmpdir}/output.zip'

    data: typing.List[reader.InputData] = [
        {'foo': 1, 'BUILDER': '4K02E90020'},
        {'bar': 2, 'baz': 3},
    ]

    extractor.write_data(data, output_path)

    with zipfile.ZipFile(output_path, 'r') as output:
        assert len(output.namelist()) == 1
