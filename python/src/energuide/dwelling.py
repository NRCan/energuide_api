import datetime
import typing
from energuide import interpreter


class NoInputDataException(Exception):
    pass


class Evaluation:

    def __init__(self, *,
                 evaluation_type: interpreter.EvaluationType,
                 entry_date: datetime.date,
                 creation_date: datetime.datetime,
                 modification_date: datetime.datetime
                ) -> None:
        self._evaluation_type = evaluation_type
        self._entry_date = entry_date
        self._creation_date = creation_date
        self._modification_date = modification_date

    @classmethod
    def from_data(cls, data: interpreter.ParsedDwellingDataRow) -> 'Evaluation':
        return Evaluation(
            evaluation_type=data.eval_type,
            entry_date=data.entry_date,
            creation_date=data.creation_date,
            modification_date=data.modification_date,
        )

    @property
    def evaluation_type(self) -> interpreter.EvaluationType:
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
                 region: interpreter.Region,
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
    def from_data(cls, data: typing.List[interpreter.ParsedDwellingDataRow]) -> 'Dwelling':
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
    def region(self) -> interpreter.Region:
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
            'region': self.region,
            'forwardSortationArea': self.forward_sortation_area,
            'evaluations': [evaluation.to_dict() for evaluation in self.evaluations]
        }
