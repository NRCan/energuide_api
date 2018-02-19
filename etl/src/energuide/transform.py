import typing
from energuide import database
from energuide import reader
from energuide import dwelling
from energuide import logging
from energuide.exceptions import InvalidEmbeddedDataTypeError
from energuide.exceptions import EnerguideError


LOGGER = logging.get_logger(__name__)


def _generate_dwellings(grouped: typing.Iterable[typing.List[reader.InputData]]) -> typing.Iterator[dwelling.Dwelling]:
    for group in grouped:
        try:
            dwell = dwelling.Dwelling.from_group(group)
            yield dwell
        except InvalidEmbeddedDataTypeError as exc:
            files = [str(file.get('jsonFileName')) for file in group]
            failing_type = exc.data_class
            LOGGER.error(f'Files: "{", ".join(files)}": {failing_type.__name__}')
        except EnerguideError as exc:
            files = [str(file.get('jsonFileName')) for file in group]
            LOGGER.error(f'Files: "{", ".join(files)}" - {exc}')


def run(coords: database.DatabaseCoordinates,
        database_name: str,
        collection: str,
        filename: str) -> None:

    raw_data = reader.read(filename)
    grouped = reader.grouper(raw_data, dwelling.Dwelling.GROUPING_FIELD)
    dwellings = _generate_dwellings(grouped)
    database.load(coords, database_name, collection, dwellings)
