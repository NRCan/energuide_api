import enum
from energuide.exceptions import InvalidInputDataError


@enum.unique
class EvaluationType(enum.Enum):
    PRE_RETROFIT = 'D'
    POST_RETROFIT = 'E'
    INCENTIVE_PROGRAM = 'F'

    @classmethod
    def from_code(cls, code: str) -> 'EvaluationType':
        if code == cls.PRE_RETROFIT.value:
            return EvaluationType.PRE_RETROFIT
        elif code == cls.POST_RETROFIT.value:
            return EvaluationType.POST_RETROFIT
        elif code == cls.INCENTIVE_PROGRAM.value:
            return EvaluationType.INCENTIVE_PROGRAM
        raise InvalidInputDataError(f'Invalid code: {code}')
