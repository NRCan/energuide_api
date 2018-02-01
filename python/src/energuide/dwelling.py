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


class _Ceiling(typing.NamedTuple):
    label: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]

    nominal_rsi: typing.Optional[float]

    effective_rsi: typing.Optional[float]

    area_metres: typing.Optional[float]
    length_metres: typing.Optional[float]


class Ceiling(_Ceiling):

    _RSI_RATIO = 5.678263337
    _FEET_SQUARED_RATIO = 10.7639
    _FEET_RATIO = 3.28084

    @classmethod
    def from_data(cls, ceiling: typing.Dict[str, typing.Any]):
        return Ceiling(
            label=ceiling['label'],
            type_english=ceiling['type_english'],
            type_french=ceiling['type_french'],
            nominal_rsi=ceiling['nominal_rsi'],

            effective_rsi=ceiling['effective_rsi'],

            area_metres=ceiling['area'],
            length_metres=ceiling['length']

        )

    def to_dict(self):
        return {
            'label': self.label,
            'type_english': self.type_english,
            'type_french': self.type_french,
            'nominal_rsi': self.nominal_rsi,
            'nominal_r': self.nominal_rsi*self._RSI_RATIO if self.nominal_rsi is not None else None,
            'effective_rsi': self.effective_rsi,
            'effective_r': self.effective_rsi*self._RSI_RATIO if self.effective_rsi is not None else None,
            'area_metres': self.area_metres,
            'area_feet': self.area_metres*self._FEET_SQUARED_RATIO if self.area_metres is not None else None,
            'length_metres': self.length_metres,
            'length_feet': self.length_metres*self._FEET_RATIO if self.length_metres is not None else None
        }


class _ParsedDwellingDataRow(typing.NamedTuple):
    eval_id: int
    eval_type: EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: datetime.datetime
    year_built: int
    city: str
    region: Region
    forward_sortation_area: str
    ceilings: typing.List[Ceiling]


class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {'type': 'string', 'required': True, 'allowed': [eval_type.value for eval_type in EvaluationType]},
        'ENTRYDATE': {'type': 'string', 'required': True},
        'CREATIONDATE': {'type': 'string', 'required': True},
        'MODIFICATIONDATE': {'type': 'string', 'required': True},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'forwardSortationArea': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z]'},
        'HOUSEREGION': {'type': 'string', 'required': True},

        'ceilings': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'dict',
                'schema': {
                    'label': {'type': 'string', 'required': True},
                    'type_english': {'type': 'string', 'required': True},
                    'type_french': {'type': 'string', 'required': True},
                    'nominal_rsi': {'type': 'float', 'required': True, 'coerce': float},
                    'effective_rsi': {'type': 'float', 'required': True, 'coerce': float},
                    'area': {'type': 'float', 'required': True, 'coerce': float},
                    'length': {'type': 'float', 'required': True, 'coerce': float}
                }
            }
        }
    }

    @classmethod
    def from_row(cls, row: reader.InputData) -> 'ParsedDwellingDataRow':
        validator = cerberus.Validator(cls._SCHEMA, allow_unknown=True)
        if not validator.validate(row):
            # import pdb; pdb.set_trace()
            error_keys = ', '.join(validator.errors.keys())
            raise reader.InvalidInputDataException(f'Validator failed on keys: {error_keys}')

        parsed = validator.document

        return ParsedDwellingDataRow(
            eval_id=parsed['EVAL_ID'],
            eval_type=EvaluationType.from_code(parsed['EVAL_TYPE']),
            entry_date=parser.parse(parsed['ENTRYDATE']).date(),
            creation_date=parser.parse(parsed['CREATIONDATE']),
            modification_date=parser.parse(parsed['MODIFICATIONDATE']),
            year_built=parsed['YEARBUILT'],
            city=parsed['CLIENTCITY'],
            region=Region.from_data(parsed['HOUSEREGION']),
            forward_sortation_area=parsed['forwardSortationArea'],
            ceilings=[Ceiling.from_data(ceiling) for ceiling in parsed['ceilings']]
        )


class Evaluation:

    def __init__(self, *,
                 evaluation_type: EvaluationType,
                 entry_date: datetime.date,
                 creation_date: datetime.datetime,
                 modification_date: datetime.datetime,
                 ceilings: typing.List[Ceiling]
                ) -> None:
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date
        self._creation_date = creation_date
        self._modification_date = modification_date
        self._ceilings = ceilings

    @classmethod
    def from_data(cls, data: ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
            ceilings=data.ceilings,
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

    @property
    def ceilings(self) -> typing.List[Ceiling]:
        return self._ceilings

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'evaluationType': self.evaluation_type.value,
            'entryDate': self.entry_date.isoformat(),
            'creationDate': self.creation_date.isoformat(),
            'modificationDate': self.modification_date.isoformat(),
            'ceilings': [ceiling.to_dict() for ceiling in self.ceilings]
        }


class Dwelling:

    GROUPING_FIELD = 'EVAL_ID'

    def __init__(self, *,
                 house_id: int,
                 year_built: int,
                 city: str,
                 region: Region,
                 forward_sortation_area: str,
                 evaluations: typing.List[Evaluation]) -> None:
        self._house_id = house_id
        self._year_built = year_built
        self._city = city
        self._region = region
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
