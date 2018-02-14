import typing
from energuide import database
from energuide import reader
from energuide import dwelling
from energuide.logging import logger


class Stats:

    def __init__(self) -> None:
        self._success = 0
        self._failure = 0

    def register_success(self) -> None:
        self._success += 1

    def register_failure(self) -> None:
        self._failure += 1

    @property
    def total(self) -> int:
        return self._success + self._failure

    @property
    def success(self) -> int:
        return self._success

    @property
    def failure(self) -> int:
        return self._failure

    def __str__(self):
        return f'Total: {self.total}\n' + \
               f'Success: {self.success}\n' + \
               f'Failure: {self.failure}'


def run(coords: database.DatabaseCoordinates,
        database_name: str,
        collection: str,
        filename: str) -> Stats:

    stats = Stats()
    def _gen_dwellings(grouped: typing.Iterable[typing.List[reader.InputData]]) -> typing.Iterator[dwelling.Dwelling]:
        for group in grouped:
            try:
                dwell = dwelling.Dwelling.from_group(group)
                stats.register_success()
                yield dwell
            except Exception as exc: # pylint: disable=broad-except
                files = [str(file.get('localFileName')) for file in group]
                logger.error(f'{", ".join(files)}: {exc}')
                stats.register_failure()

    raw_data = reader.read(filename)
    grouped = reader.grouper(raw_data, dwelling.Dwelling.GROUPING_FIELD)
    dwellings = _gen_dwellings(grouped)
    database.load(coords, database_name, collection, dwellings)

    return stats
