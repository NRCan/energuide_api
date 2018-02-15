class InvalidGroupSizeException(Exception):
    pass


class InvalidInputDataException(Exception):
    pass


class InvalidEmbeddedDataTypeException(Exception):

    def __init__(self, data_class, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_class = data_class
        self.parent = parent
