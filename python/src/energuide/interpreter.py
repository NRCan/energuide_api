import csv
import datetime
import enum
import typing
import cerberus
from dateutil import parser


class InvalidInputDataException(Exception):
    pass


InputData = typing.Dict[str, typing.Any]


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


@enum.unique
class Region(enum.Enum):
    BRITISH_COLUMBIA = 'BC'
    ALBERTA = 'AB'
    SASKATCHEWAN = 'SK'
    MANITOBA = 'MB'
    ONTARIO = 'ON'
    QUEBEC = 'QC'
    NEW_BRUNSWICK = 'NB'
    PRINCE_EDWARD_ISLAND = 'PE'
    NOVA_SCOTIA = 'NS'
    NEWFOUNDLAND_AND_LABRADOR = 'NL'
    YUKON = 'YT'
    NORTHWEST_TERRITORIES = 'NT'
    NUNAVUT = 'NU'
    UNKNOWN = '??'

    @classmethod
    def _from_name(cls, name: str) -> typing.Optional['Region']:
        snake_name = name.upper().replace(' ', '_')
        return Region[snake_name] if snake_name in Region.__members__ else None

    @classmethod
    def _from_code(cls, code: str) -> typing.Optional['Region']:
        code = code.upper()
        for region in Region:
            if code == region.value:
                return region
        return None

    @classmethod
    def from_data(cls, data: str) -> 'Region':
        output = cls._from_name(data)
        if not output:
            output = cls._from_code(data)
        if not output:
            output = Region.UNKNOWN
        return output


class _ParsedDwellingDataRow(typing.NamedTuple):
    eval_id: int
    eval_type: EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: datetime.datetime
    year_built: int
    city: str
    region: Region
    postal_code: str
    forward_sortation_area: str


class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in EvaluationType]},
        'ENTRYDATE': {'type': 'string', 'required': True},
        'CREATIONDATE': {'type': 'string', 'required': True},
        'MODIFICATIONDATE': {'type': 'string', 'required': True},
        'YEARBUILT': {'type': 'integer', 'required': True},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'CLIENTPCODE': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z] [0-9][A-Z][0-9]'},
        'HOUSEREGION': {'type': 'string', 'required': True},
    }

    @classmethod
    def from_row(cls, row: InputData) -> 'ParsedDwellingDataRow':
        validator = cerberus.Validator(cls._SCHEMA, allow_unknown=True)
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        return ParsedDwellingDataRow(
            eval_id=row['EVAL_ID'],
            eval_type=EvaluationType.from_code(row['EVAL_TYPE']),
            entry_date=parser.parse(row['ENTRYDATE']).date(),
            creation_date=parser.parse(row['CREATIONDATE']),
            modification_date=parser.parse(row['MODIFICATIONDATE']),
            year_built=row['YEARBUILT'],
            city=row['CLIENTCITY'],
            region=Region.from_data(row['HOUSEREGION']),
            postal_code=row['CLIENTPCODE'],
            forward_sortation_area=row['CLIENTPCODE'][0:3]
        )


def read(filename: str) -> typing.Iterator[InputData]:
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        #pylint: disable=stop-iteration-return
        columns = next(reader)

        def to_dict(row) -> InputData:
            return {k: v for k, v in zip(columns, row)}

        for row in reader:
            yield to_dict(row)
