import _pytest
import py
import pytest
from energuide import extractor, reader


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


def test_extract_valid(valid_filepath: str) -> None:
    output = extractor.extract(valid_filepath)
    item = dict(next(output))

    assert 'EVAL_TYPE' in item
    assert 'EVAL_ID' in item

    assert 'ENTRYBY' not in item
    assert 'CLIENTPCODE' not in item
    assert 'CLIENTNAME' not in item
    assert 'TELEPHONE' not in item
    assert 'MAIL_ADDR' not in item
    assert 'MAIL_PCODE' not in item
    assert 'TAXNUMBER' not in item
    assert 'CLIENTADDR' not in item
    assert 'RAW_XML' not in item


def test_extract_missing(invalid_filepath: str) -> None:
    with pytest.raises(reader.InvalidInputDataException) as ex:
        output = extractor.extract(invalid_filepath)
        _ = dict(next(output))

    assert 'EVAL_TYPE' not in ex.exconly()
    assert 'EVAL_ID' not in ex.exconly()

    assert 'ENTRYBY' in ex.exconly()
    assert 'CLIENTPCODE' in ex.exconly()
    assert 'CLIENTNAME' in ex.exconly()
    assert 'TELEPHONE' in ex.exconly()
    assert 'MAIL_ADDR' in ex.exconly()
    assert 'MAIL_PCODE' in ex.exconly()
    assert 'TAXNUMBER' in ex.exconly()
    assert 'CLIENTADDR' in ex.exconly()
    assert 'RAW_XML' in ex.exconly()
