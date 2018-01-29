import datetime
import pandas as pd
from energuide import database, reader, dwelling


def run(coords: database.DatabaseCoordinates,
        database_name: str,
        collection: str,
        filename: str) -> None:

    raw_data = reader.read(filename)
    grouped = reader.grouper(raw_data, dwelling.Dwelling.GROUPING_FIELD)
    dwellings = (dwelling.Dwelling.from_group(group) for group in grouped)
    database.grouped_load(coords, database_name, collection, dwellings)
