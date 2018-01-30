import typing
import os
import pytest
from energuide import extractor

@pytest.fixture
def extract_out() -> str:
    path =  os.path.join(os.path.dirname(__file__), 'randomized_energuide_data.csv')
    yield path
    os.remove(path)

def test_extract(energuide_fixture: str, extract_out: str):
    extractor.extract(energuide_fixture, extract_out)
    with open(extract_out, 'r'):
        print(extract_out.read())


