import _pytest
import pytest
from energuide.embedded import evaluation_type


class TestEvaluationType:

    codes = [
        ('D', evaluation_type.EvaluationType.PRE_RETROFIT),
        ('E', evaluation_type.EvaluationType.POST_RETROFIT),
        ('F', evaluation_type.EvaluationType.INCENTIVE_PROGRAM),
    ]

    @pytest.mark.parametrize("code, eval_type", codes)
    def test_from_code(self, code: str, eval_type: evaluation_type.EvaluationType):
        output = evaluation_type.EvaluationType.from_code(code)
        assert output == eval_type
