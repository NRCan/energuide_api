import json
import itertools
import typing
import os
import pytest
from energuide import extractor


def test_extract(energuide_fixture: str):
    with open(energuide_fixture, 'r') as file_in:
        output = extractor.extract(file_in)
        item = next(output)

        assert 'EVAL_ID' in item
        assert 'EVAL_TYPE' in item

        for coll in extractor.DROP_FIELDS:
            assert not coll in item
