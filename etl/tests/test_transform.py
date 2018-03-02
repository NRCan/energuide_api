import _pytest
import pytest
from energuide import transform
from energuide.embedded import ceiling
from energuide.exceptions import InvalidEmbeddedDataTypeError


def test_transform_no_azure(energuide_zip_fixture: str) -> None:
    output = list(transform.transform(False, energuide_zip_fixture))
    assert len(output) == 7


@pytest.mark.usefixtures('populated_azure_service')
def test_transform_azure() -> None:

    output = list(transform.transform(True, None))
    assert len(output) == 7


def test_transform_no_azure_no_filename() -> None:
    with pytest.raises(ValueError):
        list(transform.transform(False, None))


def test_bad_data(energuide_zip_fixture: str,
                  monkeypatch: _pytest.monkeypatch.MonkeyPatch,
                  capsys: _pytest.capture.CaptureFixture) -> None:

    def raise_error(*args) -> None: #pylint: disable=unused-argument
        raise InvalidEmbeddedDataTypeError(ceiling.Ceiling)

    monkeypatch.setattr(ceiling.Ceiling, 'from_data', raise_error)

    output = list(transform.transform(False, energuide_zip_fixture))
    assert not output

    _, err = capsys.readouterr()
    assert all('Ceiling' in line for line in err.split()[1:-1])
