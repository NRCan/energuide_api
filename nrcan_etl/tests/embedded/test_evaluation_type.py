from energuide.embedded import evaluation_type


class TestEvaluationType:

    def test_from_code(self):
        code = evaluation_type.EvaluationType.PRE_RETROFIT.value
        output = evaluation_type.EvaluationType.from_code(code)
        assert output == evaluation_type.EvaluationType.PRE_RETROFIT
