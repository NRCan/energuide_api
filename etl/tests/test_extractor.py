import csv
import json
import os
import typing
import zipfile
import _pytest.fixtures
import py._path.local
import pytest
from energuide import extractor
from energuide import reader
from energuide.exceptions import InvalidInputDataError


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
        'INFO1': '',
        'INFO2': '',
        'INFO3': '',
        'INFO4': '',
        'INFO5': '',
        'INFO6': '',
        'INFO7': '',
        'INFO8': '',
        'INFO9': '',
        'INFO10': '',
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


def data3() -> typing.Dict[str, typing.Optional[str]]:
    data = data1()
    data['ERSRATING'] = ''
    return data


def data4() -> typing.Dict[str, typing.Optional[str]]:
    data = data1()
    data['UNKNOWN'] = 'value'
    return data


@pytest.fixture(params=[data1(), data2(), data3()])
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
    filepath = os.path.join(tmpdir, 'sample.csv')
    data = {'EVAL_ID': 'foo', 'EVAL_TYPE': 'bar'}
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)

    return filepath


@pytest.fixture
def extra_filepath(tmpdir: py._path.local.LocalPath) -> str:
    filepath = os.path.join(tmpdir, 'sample.csv')

    data = data4()
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)

    return filepath


def test_extract_valid(valid_filepath: str) -> None:
    output = extractor.extract_data(valid_filepath)
    item = dict(next(output))

    assert 'EVAL_ID' in item

    assert 'CLIENTADDR' not in item


def test_purge_unknown(extra_filepath: str) -> None:
    output = extractor.extract_data(extra_filepath)
    item = dict(next(output))

    assert 'UNKNOWN' not in item


def test_extract_missing(invalid_filepath: str) -> None:
    with pytest.raises(InvalidInputDataError) as ex:
        output = extractor.extract_data(invalid_filepath)
        dict(next(output))

    assert 'EVAL_ID' not in ex.exconly()
    assert 'BUILDER' in ex.exconly()


def test_empty_to_none(tmpdir: py._path.local.LocalPath) -> None:
    filepath = os.path.join(tmpdir, 'sample.csv')
    data = data3()
    with open(filepath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)

    output = extractor.extract_data(filepath)
    row = next(output)
    assert row['ERSRATING'] is None


def test_extract_with_snippets(tmpdir: py._path.local.LocalPath) -> None:
    xml_data = """
<HouseFile><House><Components><Ceiling>
    <Label>Attic</Label>
    <Construction>
        <Type>
            <English>Attic/gable</English>
            <French>Combles/pignon</French>
        </Type>
        <CeilingType idref="Code 3" rValue="2.9463" nominalInsulation="2.864">2401191000</CeilingType>
    </Construction>
</Ceiling></Components></House></HouseFile>
    """

    data = data1()
    data['RAW_XML'] = xml_data

    input_file = tmpdir.join('input.csv')
    with open(input_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)

    output = list(extractor.extract_data(str(input_file)))
    assert output[0]['ceilings']


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
