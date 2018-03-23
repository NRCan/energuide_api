import os
import py
import pytest
from energuide import extractor


@pytest.fixture
def energuide_fixture() -> str:
    return os.path.join(os.path.dirname(__file__), 'scrubbed_random_sample_xml.csv')


@pytest.fixture
def energuide_zip_fixture(tmpdir: py._path.local.LocalPath, energuide_fixture: str) -> str:
    outfile = os.path.join(tmpdir, 'scrubbed_random_sample_xml.zip')

    data = extractor.extract_data(energuide_fixture)
    extractor.write_data(data, outfile)
    return outfile
