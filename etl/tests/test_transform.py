import typing
import _pytest
import pytest
from energuide import transform
from energuide.embedded import ceiling
from energuide.exceptions import InvalidEmbeddedDataTypeError


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

    assert len(output) == 14
    assert output[0]['BUILDER'] == '11W2D00606'
    assert len(unique_builders) == 14


def test_reader_sorted_by_eval_id(local_reader: transform.LocalExtractReader) -> None:
    output = list(local_reader.extracted_rows())

    assert all(
        typing.cast(str, row.get('EVAL_ID')) <= typing.cast(str, next.get('EVAL_ID'))
        for row, next in zip(output, output[1:])
    )


def test_reader_num_rows(local_reader: transform.LocalExtractReader) -> None:
    assert local_reader.num_rows() == 14


def test_azure_reader(azure_reader: transform.AzureExtractReader) -> None:
    output = list(azure_reader.extracted_rows())
    output = sorted(output, key=lambda row: row['BUILDER'])
    unique_builders = {row['BUILDER'] for row in output}
    assert len(output) == 14
    assert output[0]['BUILDER'] == '11W2D00606'
    assert len(unique_builders) == 14


def test_azure_reader_num_rows(azure_reader: transform.AzureExtractReader) -> None:
    assert azure_reader.num_rows() == 14


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
    assert len(list(output)) == 7


def test_bad_data(local_reader: transform.LocalExtractReader,
                  monkeypatch: _pytest.monkeypatch.MonkeyPatch,
                  capsys: _pytest.capture.CaptureFixture) -> None:

    def raise_error(*args) -> None: #pylint: disable=unused-argument
        raise InvalidEmbeddedDataTypeError(ceiling.Ceiling)

    monkeypatch.setattr(ceiling.Ceiling, 'from_data', raise_error)

    output = list(transform.transform(local_reader))
    assert not output

    _, err = capsys.readouterr()
    assert all('Ceiling' in line for line in err.split()[1:-1])
