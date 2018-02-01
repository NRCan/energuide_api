import pytest
from energuide import reader
from energuide import extracted_datatypes


# pylint: disable=no-self-use


@pytest.fixture
def ceiling_input() -> reader.InputData:
    return {
        'label': 'Main attic',
        'typeEnglish': 'Attic/gable',
        'typeFrench': 'Combles/pignon',
        'nominalRsi': '2.864',
        'effectiveRsi': '2.9463',
        'area': '46.4515',
        'length': '23.875',
    }


@pytest.fixture
def floor_input() -> reader.InputData:
    return {
        'label': 'Rm over garage',
        'nominalRsi': '2.46',
        'effectiveRsi': '2.9181',
        'area': '9.2903',
        'length': '3.048',
    }


@pytest.fixture
def sample_input_d(ceiling_input: reader.InputData,
                   floor_input: reader.InputData) -> reader.InputData:
    return {
        'EVAL_ID': '123',
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Ottawa',
        'forwardSortationArea': 'K1P',
        'HOUSEREGION': 'Ontario',
        'YEARBUILT': '2000',
        'ceilings': [
            ceiling_input
        ],
        'floors': [
            floor_input
        ]
    }


class TestCeiling:

    @pytest.fixture
    def sample(self, sample_input_d: reader.InputData):
        ceiling = sample_input_d['ceilings'][0]
        ceiling['nominalRsi'] = float(ceiling['nominalRsi'])
        ceiling['effectiveRsi'] = float(ceiling['effectiveRsi'])
        ceiling['area'] = float(ceiling['area'])
        ceiling['length'] = float(ceiling['length'])
        return ceiling

    def test_from_data(self, sample):
        output = extracted_datatypes.Ceiling.from_data(sample)
        assert output.label == 'Main attic'
        assert output.area_metres == 46.4515


class TestFloor:

    @pytest.fixture
    def sample(self, sample_input_d: reader.InputData):
        floor = sample_input_d['floors'][0]
        floor['nominalRsi'] = float(floor['nominalRsi'])
        floor['effectiveRsi'] = float(floor['effectiveRsi'])
        floor['area'] = float(floor['area'])
        floor['length'] = float(floor['length'])
        return floor

    def test_from_data(self, sample):
        output = extracted_datatypes.Floor.from_data(sample)
        assert output.label == 'Rm over garage'
        assert output.area_metres == 9.2903
