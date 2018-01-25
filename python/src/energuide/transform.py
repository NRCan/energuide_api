import pandas as pd
from energuide import database


CHUNKSIZE = 1000


def clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.where((pd.notnull(dataframe)), None)


def run(coords: database.DatabaseCoordinates, database_name: str, collection: str, filename: str) -> None:
    chunks = pd.read_csv(filename, chunksize=CHUNKSIZE)

    for chunk in chunks:
        cleaned = clean(chunk)
        database.load(coords, database_name, collection, cleaned)
