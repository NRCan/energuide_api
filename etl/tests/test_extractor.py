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
        'EVAL_TYPE': 'D',
        'RAW_XML': """
<HouseFile>
</HouseFile>
        """,
        'BUILDER': '4K13D01404',
        'ENTRYDATE': '2012-02-25',
        'CREATIONDATE': '2012-06-08 09:26:10',
        'MODIFICATIONDATE': '2012-06-09 09:26:10',
        'YEARBUILT': '1894',
        'CLIENTCITY': 'Brooks',
        'HOUSEREGION': 'AB',
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


def test_extract_with_snippets(tmpdir: py._path.local.LocalPath, base_data: typing.Dict[str, str]) -> None:
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

    base_data['RAW_XML'] = xml_data

    input_file = tmpdir.join('input.csv')
    with open(input_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(base_data.keys()))
        writer.writeheader()
        writer.writerow(base_data)

    output = next(extractor.extract_data(str(input_file)))
    assert output
    assert output['ceilings']


def test_extract_with_tsv_snippets(tmpdir: py._path.local.LocalPath, base_data: typing.Dict[str, str]) -> None:
    xml_data = """
<HouseFile>
    <ProgramInformation>
        <Client>
            <StreetAddress>
                <PostalCode>H0H 0H0</PostalCode>
            </StreetAddress>
        </Client>
    </ProgramInformation>
    <Program>
        <Results>
            <Tsv>
                <ERSRating value='257' />
            </Tsv>
        </Results>
    </Program>
</HouseFile>
    """
    base_data['RAW_XML'] = xml_data

    input_file = tmpdir.join('input.csv')
    with open(input_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(base_data.keys()))
        writer.writeheader()
        writer.writerow(base_data)

    output = next(extractor.extract_data(str(input_file)))
    assert output
    assert output['ersRating'] == '257'
    assert output['forwardSortationArea'] == 'H0H'


def test_write_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = f'{tmpdir}/output.zip'

    data = [
        {'foo': 1, 'BUILDER': '4K02E90020'},
        {'bar': 2, 'baz': 3, 'BUILDER': '4K13D01404'},
    ]

    result = extractor.write_data(data, output_path)
    assert result == (2, 0)

    with zipfile.ZipFile(output_path, 'r') as output_file:
        files = [output_file.read('4K02E90020'), output_file.read('4K13D01404')]

    assert [json.loads(file) for file in files] == data


def test_write_bad_data(tmpdir: py._path.local.LocalPath) -> None:
    output_path = f'{tmpdir}/output.zip'

    data: typing.List[typing.Dict[str, typing.Any]] = [
        {'foo': 1, 'BUILDER': '4K02E90020'},
        {'bar': 2, 'baz': 3},
    ]

    extractor.write_data(data, output_path)

    with zipfile.ZipFile(output_path, 'r') as output:
        assert len(output.namelist()) == 1
