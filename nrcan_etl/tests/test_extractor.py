import csv
import json
import os
import typing
import zipfile
import _pytest.fixtures
import py._path.local
import pytest
from energuide import extractor


def _write_csv(filepath: str, data: typing.Mapping[str, typing.Optional[str]]) -> None:
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(dict(data))


@pytest.fixture
def base_data() -> typing.Dict[str, str]:
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
        'CLIENTPCODE': 'L1R5C7',
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

        'EGHRATING': '50.0',
        'UGRRATING': '49.5',

        'WALLDEF': '45.3;12;50;12;4.7;12',
        'UGRWALLDEF': '45.3;12;50;12;4.7;10',
        'EGHHLWALLS': '27799.9',
        'UGRHLWALLS': '27799.9',

        'RAW_XML': '',
    }


@pytest.fixture
def extra_data() -> typing.Dict[str, str]:
    data = base_data()
    data['other_1'] = 'foo'
    data['other_2'] = 'bar'
    return data


@pytest.fixture
def missing_data() -> typing.Dict[str, str]:
    data = base_data()
    data.pop('BUILDER')
    return data


@pytest.fixture
def nullable_data() -> typing.Dict[str, typing.Optional[str]]:
    data = base_data()
    data['MODIFICATIONDATE'] = None
    return data


@pytest.fixture(params=[base_data(), extra_data()])
def valid_filepath(tmpdir: py._path.local.LocalPath, request: _pytest.fixtures.SubRequest) -> str:
    data_dict = typing.cast(typing.Dict[str, str], request.param)
    filepath = os.path.join(tmpdir, 'sample.csv')
    _write_csv(filepath, data_dict)
    return filepath


@pytest.fixture
def missing_filepath(tmpdir: py._path.local.LocalPath, missing_data: typing.Dict[str, str]) -> str:
    filepath = os.path.join(tmpdir, 'sample.csv')
    _write_csv(filepath, missing_data)
    return filepath


@pytest.fixture
def extra_filepath(tmpdir: py._path.local.LocalPath, extra_data: typing.Dict[str, str]) -> str:
    filepath = os.path.join(tmpdir, 'sample.csv')
    _write_csv(filepath, extra_data)
    return filepath


def test_extract_valid(valid_filepath: str) -> None:
    output = next(extractor.extract_data(valid_filepath))
    assert output
    item = dict(output)
    assert 'EVAL_ID' in item


def test_purge_unknown(extra_filepath: str) -> None:
    output = next(extractor.extract_data(extra_filepath))
    assert output
    item = dict(output)
    assert 'other_1' not in item


def test_extract_missing(missing_filepath: str) -> None:
    output = extractor.extract_data(missing_filepath)
    result = [x for x in output]
    assert result == [None]


def test_empty_to_none(tmpdir: py._path.local.LocalPath, nullable_data: typing.Dict[str, typing.Optional[str]]) -> None:
    filepath = os.path.join(tmpdir, 'sample.csv')
    _write_csv(filepath, nullable_data)
    output = extractor.extract_data(filepath)
    row = next(output)
    assert row
    assert row['MODIFICATIONDATE'] is None


def test_write_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = os.path.join(tmpdir, 'output.zip')

    data = [
        {'foo': 1, 'BUILDER': '4K02E90020', 'EVAL_ID': '12149', 'HOUSE_ID': '15678'},
        {'bar': 2, 'baz': 3, 'BUILDER': '4K13D01404', 'EVAL_ID': '12148', 'HOUSE_ID': '15678'},
    ]

    result = extractor.write_data(data, output_path)
    assert result == (2, 0)

    with zipfile.ZipFile(output_path, 'r') as output_file:
        files = [output_file.read('15678-12149-4K02E90020'), output_file.read('15678-12148-4K13D01404')]

    assert [json.loads(file) for file in files] == data


def test_write_bad_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = os.path.join(tmpdir, 'output.zip')

    data: typing.List[typing.Dict[str, typing.Any]] = [
        {'foo': 1, 'BUILDER': '4K02E90020', 'EVAL_ID': '12148', 'HOUSE_ID': '15678'},
        {'bar': 2, 'baz': 3},
    ]

    extractor.write_data(data, output_path)

    with zipfile.ZipFile(output_path, 'r') as output:
        assert len(output.namelist()) == 1
