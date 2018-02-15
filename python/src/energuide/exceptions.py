import typing

class EnerguideException(Exception):
    pass


class InvalidGroupSizeException(EnerguideException):
    pass


class InvalidInputDataException(EnerguideException):
    pass


class InvalidEmbeddedDataTypeException(EnerguideException):

    def __init__(self, data_class: type, *args: typing.Tuple, **kwargs: typing.Dict) -> None:
        super().__init__(*args, **kwargs)
        self.data_class = data_class
