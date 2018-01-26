import datetime
from dateutil import parser
import enum
import typing
import cerberus


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

    def __init__(self, *,
                 evaluation_type: EvaluationType,
                 entry_date: datetime.date,
                 ) -> None:
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date

    SCHEMA = {
        'EVAL_TYPE': {'type': 'string', 'required': True},
        'ENTRYDATE': {'type': 'string', 'required': True},
    }

    @classmethod
    def from_data(cls, data: EvaluationData) -> 'Evaluation':
        validator = cerberus.Validator(cls.SCHEMA, allow_unknown=True)
        if not validator.validate(data):
            raise InvalidInputDataException()

        eval_type = EvaluationType.from_code(data['EVAL_TYPE'])
        return Evaluation(
            evaluation_type=eval_type,
            entry_date=parser.parse(data['ENTRYDATE']).date(),
        )

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type

    @property
    def entry_date(self) -> datetime.date:
        return self._entry_date


class Dwelling:

    def __init__(self, *,
                 house_id: int,
                 evaluations: typing.List[Evaluation]) -> None:
        self._house_id = house_id
        self._evaluations = evaluations

    SCHEMA = {
        'EVAL_TYPE': {'type': 'string', 'required': True},
    }

    @classmethod
    def from_data(cls, data: DwellingData) -> 'Dwelling':
        data = list(data)
        if data:
            validator = cerberus.Validator(cls.SCHEMA, allow_unknown=True)

            if not all([validator.validate(row) for row in data]):
                raise InvalidInputDataException()

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
