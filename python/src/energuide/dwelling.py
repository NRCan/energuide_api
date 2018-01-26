import typing


class NoInputDataException(Exception):
    pass


class InvalidInputDataException(Exception):
    pass


DwellingData = typing.Iterable[typing.Dict[str, typing.Any]]


class Dwelling:

    def __init__(self, *, house_id: int) -> None:
        self._house_id = house_id

    @staticmethod
    def verify_schema(data: DwellingData):
        for row in data:
            if 'EVAL_ID' not in row.keys():
                raise InvalidInputDataException()

    @classmethod
    def from_data(cls, data: DwellingData) -> 'Dwelling':
        data = list(data)
        if data:
            cls.verify_schema(data)
            house_id = data[0]['EVAL_ID']
            return Dwelling(house_id=house_id)
        else:
            raise NoInputDataException()

    @property
    def house_id(self) -> int:
        return self._house_id
