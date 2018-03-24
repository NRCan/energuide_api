import datetime
import enum
import typing
from dateutil import parser
from energuide import validator
from energuide.embedded import upgrade
from energuide.embedded import measurement
from energuide.embedded import walls
from energuide.embedded import region
from energuide.embedded import evaluation_type
from energuide.exceptions import InvalidGroupSizeError
from energuide.exceptions import InvalidInputDataError


class _ParsedDwellingDataRow(typing.NamedTuple):
    house_id: int
    eval_id: int
    file_id: str
    eval_type: evaluation_type.EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: typing.Optional[datetime.datetime]
    year_built: int
    city: str
    region: region.Region
    forward_sortation_area: str
    house_type: str

    energy_upgrades: typing.List[upgrade.Upgrade]
    heated_floor_area: typing.Optional[float]
    egh_rating: measurement.Measurement
    ers_rating: measurement.Measurement
    greenhouse_gas_emissions: measurement.Measurement
    energy_intensity: measurement.Measurement

    walls: measurement.Measurement


class ParsedDwellingDataRow(_ParsedDwellingDataRow):

    _SCHEMA = {
        'EVAL_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'HOUSE_ID': {'type': 'integer', 'required': True, 'coerce': int},
        'EVAL_TYPE': {
            'type': 'string',
            'required': True,
            'allowed': [eval_type.value for eval_type in evaluation_type.EvaluationType]
        },
        'ENTRYDATE': {'type': 'date', 'required': True, 'coerce': parser.parse},
        'CREATIONDATE': {'type': 'datetime', 'required': True, 'coerce': parser.parse},
        'YEARBUILT': {'type': 'integer', 'required': True, 'coerce': int},
        'CLIENTCITY': {'type': 'string', 'required': True},
        'forwardSortationArea': {'type': 'string', 'required': True, 'regex': '[A-Z][0-9][A-Z]'},
        'HOUSEREGION': {'type': 'string', 'required': True},
        'BUILDER': {'type': 'string', 'required': True},

        'upgrades': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'xml',
                'coerce': 'parse_xml',
            }
        },

        'MODIFICATIONDATE': {'type': 'datetime', 'nullable': True, 'required': True, 'coerce': parser.parse},

        'HEATEDFLOORAREA': {'type': 'float', 'nullable': True, 'coerce': float},
        'TYPEOFHOUSE': {'type': 'string', 'nullable': True},

        'EGHRATING': {'type': 'integer', 'nullable': True, 'coerce': int},
        'UGRRATING': {'type': 'integer', 'nullable': True, 'coerce': int},

        'ERSRATING': {'type': 'integer', 'nullable': True, 'coerce': int},
        'UGRERSRATING': {'type': 'integer', 'nullable': True, 'coerce': int},

        'ERSGHG': {'type': 'float', 'nullable': True, 'coerce': float},
        'UGRERSGHG': {'type': 'float', 'nullable': True, 'coerce': float},

        'ERSENERGYINTENSITY': {'type': 'float', 'nullable': True, 'coerce': float},
        'UGRERSENERGYINTENSITY': {'type': 'float', 'nullable': True, 'coerce': float},

        'WALLDEF': {'type': 'string', 'nullable': True, 'required': True},
        'UGRWALLDEF': {'type': 'string', 'nullable': True, 'required': True},
        'EGHHLWALLS': {'type': 'float', 'nullable': True, 'required': True, 'coerce': float},
        'UGRHLWALLS': {'type': 'float', 'nullable': True, 'required': True, 'coerce': float},
    }

    @classmethod
    def from_row(cls, row: typing.Dict[str, typing.Any]) -> 'ParsedDwellingDataRow':
        checker = validator.DwellingValidator(cls._SCHEMA, allow_unknown=True)
        if not checker.validate(row):
            error_keys = ', '.join(checker.errors.keys())
            raise InvalidInputDataError(f'Validator failed on keys: {error_keys}')

        parsed = checker.document

        return ParsedDwellingDataRow(
            house_id=parsed['HOUSE_ID'],
            eval_id=parsed['EVAL_ID'],
            file_id=parsed['BUILDER'],
            eval_type=evaluation_type.EvaluationType.from_code(parsed['EVAL_TYPE']),
            entry_date=parsed['ENTRYDATE'].date(),
            creation_date=parsed['CREATIONDATE'],
            modification_date=parsed['MODIFICATIONDATE'],
            year_built=parsed['YEARBUILT'],
            city=parsed['CLIENTCITY'],
            region=region.Region.from_data(parsed['HOUSEREGION']),
            forward_sortation_area=parsed['forwardSortationArea'],

            energy_upgrades=[upgrade.Upgrade.from_data(upgrade_node) for upgrade_node in parsed['upgrades']],
            heated_floor_area=parsed['HEATEDFLOORAREA'],
            house_type=parsed['TYPEOFHOUSE'],

            egh_rating=measurement.Measurement(
                measurement=parsed['EGHRATING'],
                upgrade=parsed['UGRRATING'],
            ),

            ers_rating=measurement.Measurement(
                measurement=parsed['ERSRATING'],
                upgrade=parsed['UGRERSRATING'],
            ),

            greenhouse_gas_emissions=measurement.Measurement(
                measurement=parsed['ERSGHG'],
                upgrade=parsed['UGRERSGHG'],
            ),

            energy_intensity=measurement.Measurement(
                measurement=parsed['ERSENERGYINTENSITY'],
                upgrade=parsed['UGRERSENERGYINTENSITY'],
            ),

            walls=measurement.Measurement(
                measurement=walls.Wall.from_data(
                    parsed['WALLDEF'],
                    parsed['EGHHLWALLS'],
                ),
                upgrade=walls.Wall.from_data(
                    parsed['UGRWALLDEF'],
                    parsed['UGRHLWALLS'],
                ),
            )
        )


class _Evaluation(typing.NamedTuple):
    file_id: str
    evaluation_id: int
    evaluation_type: evaluation_type.EvaluationType
    entry_date: datetime.date
    creation_date: datetime.datetime
    modification_date: typing.Optional[datetime.datetime]
    house_type: str
    energy_upgrades: typing.List[upgrade.Upgrade]
    heated_floor_area: measurement.Measurement
    egh_rating: measurement.Measurement
    ers_rating: measurement.Measurement
    greenhouse_gas_emissions: measurement.Measurement
    energy_intensity: measurement.Measurement
    walls: measurement.Measurement


class Evaluation(_Evaluation):

    @classmethod
    def from_data(cls, data: ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            file_id=data.file_id,
            evaluation_id=data.eval_id,
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
            energy_upgrades=data.energy_upgrades,
            heated_floor_area=data.heated_floor_area,
            house_type=data.house_type,
            egh_rating=data.egh_rating,
            ers_rating=data.ers_rating,
            greenhouse_gas_emissions=data.greenhouse_gas_emissions,
            energy_intensity=data.energy_intensity,
            walls=data.walls,

        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'fileId': self.file_id,
            'evaluationId': self.evaluation_id,
            'evaluationType': self.evaluation_type.value,
            'entryDate': self.entry_date.isoformat(),
            'creationDate': self.creation_date.isoformat(),
            'modificationDate': self.modification_date.isoformat() if self.modification_date is not None else None,
            'energyUpgrades': [upgrade.to_dict() for upgrade in self.energy_upgrades],
            'heated_floor_area': self.heated_floor_area,
            'egh_rating': self.egh_rating.to_dict(),
            'ers_rating': self.ers_rating.to_dict(),
            'greenhouse_gas_emissions': self.greenhouse_gas_emissions.to_dict(),
            'energy_intensity': self.energy_intensity.to_dict(),
            'walls': self.walls.to_dict(),
        }


def _filter_dummy_evaluations(data: typing.List[ParsedDwellingDataRow]) -> typing.List[ParsedDwellingDataRow]:
    pre_evals = {
        evaluation.entry_date: evaluation
        for evaluation in data if evaluation.eval_type is evaluation_type.EvaluationType.PRE_RETROFIT
    }
    post_evals = {
        evaluation.entry_date: evaluation
        for evaluation in data if evaluation.eval_type is evaluation_type.EvaluationType.POST_RETROFIT
    }

    return list(post_evals.values()) + \
           [evaluation for date, evaluation in pre_evals.items() if date not in post_evals.keys()]


class _Dwelling(typing.NamedTuple):
    house_id: int
    house_type: str
    year_built: int
    city: str
    region: region.Region
    forward_sortation_area: str
    evaluations: typing.List[Evaluation]


class Dwelling(_Dwelling):

    GROUPING_FIELD = 'HOUSE_ID'


    @classmethod
    def _from_parsed_group(cls, data: typing.List[ParsedDwellingDataRow]) -> 'Dwelling':
        if not data:
            raise InvalidGroupSizeError('Empty groups are invalid')


        evaluations = [Evaluation.from_data(row) for row in _filter_dummy_evaluations(data)]
        return Dwelling(
            house_id=data[0].house_id,
            house_type=data[0].house_type,
            year_built=data[0].year_built,
            city=data[0].city,
            region=data[0].region,
            forward_sortation_area=data[0].forward_sortation_area,
            evaluations=evaluations,
        )

    @classmethod
    def from_group(cls, data: typing.List[typing.Dict[str, typing.Any]]) -> 'Dwelling':
        parsed_data = [ParsedDwellingDataRow.from_row(row) for row in data]
        return cls._from_parsed_group(parsed_data)


    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'houseId': self.house_id,
            'houseType': self.house_type,
            'yearBuilt': self.year_built,
            'city': self.city,
            'region': self.region.value,
            'forwardSortationArea': self.forward_sortation_area,
            'evaluations': [evaluation.to_dict() for evaluation in self.evaluations]
        }
