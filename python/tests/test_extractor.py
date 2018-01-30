import json
import typing
import os
import pytest
from energuide import extractor


def test_extract(energuide_fixture: str):
    output = extractor.extract(energuide_fixture, extract_out)

    for row in output:
        print(row)

    assert False


