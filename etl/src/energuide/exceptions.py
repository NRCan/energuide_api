import typing


class EnerguideError(Exception):
    pass


class InvalidGroupSizeError(EnerguideError):
    pass


class InvalidInputDataError(EnerguideError):
    pass


class InvalidEmbeddedDataTypeError(EnerguideError):

    def __init__(self, data_class: type, *args: typing.Tuple, **kwargs: typing.Dict) -> None:
        super().__init__(*args, **kwargs)
        self.data_class = data_class
