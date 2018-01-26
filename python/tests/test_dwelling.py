import datetime
import typing
import pytest
from energuide import dwelling

# pylint: disable=no-self-use


@pytest.fixture
def sample_eval_d() -> dwelling.EvaluationData:
    return {
        'EVAL_ID': 123,
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
    }


@pytest.fixture
def sample_eval_e() -> dwelling.EvaluationData:
    return {
        'EVAL_ID': 123,
        'EVAL_TYPE': 'E',
        'ENTRYDATE': '2018-02-01',
        'CREATIONDATE': '2018-02-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
    }


class TestEvaluationType:

    def test_from_code(self):
        code = dwelling.EvaluationType.PRE_RETROFIT.value
        output = dwelling.EvaluationType.from_code(code)
        assert output == dwelling.EvaluationType.PRE_RETROFIT


class TestDwellingEvaluation:

    def test_eval_type(self, sample_eval_d: dwelling.EvaluationData) -> None:
        output = dwelling.Evaluation.from_data(sample_eval_d)
        assert output.evaluation_type == dwelling.EvaluationType.PRE_RETROFIT

    def test_entry_date(self, sample_eval_d: dwelling.EvaluationData) -> None:
        output = dwelling.Evaluation.from_data(sample_eval_d)
        assert output.entry_date == datetime.date(2018, 1, 1)

    def test_creation_date(self, sample_eval_d: dwelling.EvaluationData) -> None:
        output = dwelling.Evaluation.from_data(sample_eval_d)
        assert output.creation_date == datetime.datetime(2018, 1, 8, 9)

    def test_modification_date(self, sample_eval_d: dwelling.EvaluationData) -> None:
        output = dwelling.Evaluation.from_data(sample_eval_d)
        assert output.modification_date == datetime.datetime(2018, 6, 1, 9)

    def test_no_data(self) -> None:
        data: dwelling.EvaluationData = {}
        with pytest.raises(dwelling.InvalidInputDataException):
            dwelling.Evaluation.from_data(data)

    def test_bad_data(self) -> None:
        data: dwelling.EvaluationData = {'foo': 'Q'}
        with pytest.raises(dwelling.InvalidInputDataException):
            dwelling.Evaluation.from_data(data)


class TestDwelling:

    @pytest.fixture
    def sample(self,
               sample_eval_d: dwelling.EvaluationData,
               sample_eval_e: dwelling.EvaluationData) -> dwelling.DwellingData:
        return [sample_eval_d, sample_eval_e]

    def test_house_id(self, sample: dwelling.DwellingData) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert output.house_id == 123

    def test_evaluations(self,
                         sample: dwelling.DwellingData) -> None:
        output = dwelling.Dwelling.from_data(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(dwelling.NoInputDataException):
            dwelling.Dwelling.from_data(data)

    def test_bad_data(self) -> None:
        data = [{'foo': 123}]
        with pytest.raises(dwelling.InvalidInputDataException):
            dwelling.Dwelling.from_data(data)
