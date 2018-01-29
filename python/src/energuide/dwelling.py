import datetime
import enum
import typing
from dateutil import parser
import cerberus
from energuide import reader


class NoInputDataException(Exception):
    pass


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
            raise reader.InvalidInputDataException()


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
    def from_row(cls, row: reader.InputData) -> 'ParsedDwellingDataRow':
        validator = cerberus.Validator(cls._SCHEMA, allow_unknown=True)
        if not validator.validate(row):
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')

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


class Evaluation:

    def __init__(self, *,
                 evaluation_type: EvaluationType,
                 entry_date: datetime.date,
                 creation_date: datetime.datetime,
                 modification_date: datetime.datetime
                ) -> None:
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date
        self._creation_date = creation_date
        self._modification_date = modification_date

    @classmethod
    def from_data(cls, data: ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
        )

    @property
    def evaluation_type(self) -> EvaluationType:
        return self._evaluation_type

    @property
    def entry_date(self) -> datetime.date:
        return self._entry_date

    @property
    def creation_date(self) -> datetime.datetime:
        return self._creation_date

    @property
    def modification_date(self) -> datetime.datetime:
        return self._modification_date

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'evaluationType': self.evaluation_type,
            'entryDate': self.entry_date,
            'creationDate': self.creation_date,
            'modificationDate': self.modification_date,
        }


class Dwelling:

    def __init__(self, *,
                 house_id: int,
                 year_built: int,
                 city: str,
                 region: Region,
                 postal_code: str,
                 forward_sortation_area: str,
                 evaluations: typing.List[Evaluation]) -> None:
        self._house_id = house_id
        self._year_built = year_built
        self._city = city
        self._region = region
        self._postal_code = postal_code
        self._forward_sortation_area = forward_sortation_area
        self._evaluations = evaluations

    @classmethod
    def _from_parsed_group(cls, data: typing.List[ParsedDwellingDataRow]) -> 'Dwelling':
        if data:
            evaluations = [Evaluation.from_data(row) for row in data]
            return Dwelling(
                house_id=data[0].eval_id,
                year_built=data[0].year_built,
                city=data[0].city,
                region=data[0].region,
                postal_code=data[0].postal_code,
                forward_sortation_area=data[0].forward_sortation_area,
                evaluations=evaluations,
            )
        else:
            raise NoInputDataException()

    @classmethod
    def from_group(cls, data: typing.List[reader.InputData]) -> 'Dwelling':
        parsed_data = [ParsedDwellingDataRow.from_row(row) for row in data]
        return cls._from_parsed_group(parsed_data)

    @property
    def house_id(self) -> int:
        return self._house_id

    @property
    def year_built(self) -> int:
        return self._year_built

    @property
    def city(self) -> str:
        return self._city

    @property
    def region(self) -> Region:
        return self._region

    @property
    def postal_code(self) -> str:
        return self._postal_code

    @property
    def forward_sortation_area(self) -> str:
        return self._forward_sortation_area

    @property
    def evaluations(self) -> typing.List[Evaluation]:
        return self._evaluations

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'houseId': self.house_id,
            'yearBuilt': self.year_built,
            'city': self.city,
            'region': self.region.value,
            'forwardSortationArea': self.forward_sortation_area,
            'evaluations': [evaluation.to_dict() for evaluation in self.evaluations]
        }
