import typing


class EnerguideError(Exception):
    pass


class InvalidGroupSizeError(EnerguideError):
    pass


class InvalidInputDataError(EnerguideError):
    pass


class InvalidEmbeddedDataTypeError(EnerguideError):

    def __init__(self, data_class: type, msg: typing.Optional[str] = None) -> None:
        self.data_class = data_class

        if msg:
            super().__init__(msg)
        else:
            super().__init__()

class ElementGetValueError(EnerguideError):
    pass
