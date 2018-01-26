import enum
import typing


class NoInputDataException(Exception):
    pass


class InvalidInputDataException(Exception):
    pass


EvaluationData = typing.Dict[str, typing.Any]
DwellingData = typing.Iterable[EvaluationData]


@enum.unique
class EvaluationType(enum.Enum):
    PRE_RETROFIT = 'D'
    POST_RETROFIT = 'E'

    @classmethod
    def from_code(cls, code: str) -> 'EvaluationType':
        if code == cls.PRE_RETROFIT.value:
            return EvaluationType.PRE_RETROFIT
        elif code == cls.POST_RETROFIT.value:
            return EvaluationType.POST_RETROFIT
        else:
            raise InvalidInputDataException()


class Evaluation:

    def __init__(self, *, evaluation_type: EvaluationType) -> None:
        self._evaluation_type = evaluation_type

    @staticmethod
    def _verify_schema(data: EvaluationData):
        if 'EVAL_TYPE' not in data.keys():
            raise InvalidInputDataException()

    @classmethod
    def from_data(cls, data: EvaluationData) -> 'Evaluation':
        cls._verify_schema(data)
        eval_type = EvaluationType.from_code(data['EVAL_TYPE'])
        return Evaluation(evaluation_type=eval_type)

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type


class Dwelling:

    def __init__(self, *,
                 house_id: int,
                 evaluations: typing.List[Evaluation]) -> None:
        self._house_id = house_id
        self._evaluations = evaluations

    @staticmethod
    def _verify_schema(data: DwellingData):
        for row in data:
            if 'EVAL_ID' not in row.keys():
                raise InvalidInputDataException()

    @classmethod
    def from_data(cls, data: DwellingData) -> 'Dwelling':
        data = list(data)
        if data:
            cls._verify_schema(data)
            house_id = data[0]['EVAL_ID']
            evaluations = [Evaluation.from_data(row) for row in data]
            return Dwelling(
                house_id=house_id,
                evaluations=evaluations,
            )
        else:
            raise NoInputDataException()

    @property
    def house_id(self) -> int:
        return self._house_id

    @property
    def evaluations(self) -> typing.List[Evaluation]:
        return self._evaluations
