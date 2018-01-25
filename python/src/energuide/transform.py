import datetime
import pandas as pd
from energuide import database


CHUNKSIZE = 1000

_COLUMN_MAPPING = {
    'EVAL_ID': 'evalId',
    'IDNUMBER': 'idNumber',
    'CREATIONDATE': 'creationDate',
    'MODIFICATIONDATE': 'modificationDate',
    'YEARBUILT': 'yearBuilt',
    'HOUSEREGION': 'houseRegion',
    'CLIENTCITY': 'clientCity',
    'CLIENTPCODE': 'clientPostalCode'
}


def clear_blanks(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.where((pd.notnull(dataframe)), None)


def rename_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.rename(columns=_COLUMN_MAPPING, inplace=True)

    return dataframe


def extract_postal(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.loc[:, 'clientForwardSortationArea'] = dataframe['clientPostalCode'].str[:3]

    return dataframe


def parse_date_string(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def parse_dates(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['creationDate'] = dataframe['creationDate'].apply(parse_date_string)
    dataframe['modificationDate'] = dataframe['modificationDate'].apply(parse_date_string)

    return dataframe


def group_dates(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['evaluations'] = [[x] for x in dataframe[['creationDate', 'modificationDate']].to_dict('records')]
    del dataframe['creationDate']
    del dataframe['modificationDate']

    return dataframe


TRANSFORMERS = [
    clear_blanks,
    rename_columns,
    extract_postal,
    parse_dates,
    group_dates
]


def clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    for transformation in TRANSFORMERS:
        dataframe = transformation(dataframe)

    return dataframe


def run(coords: database.DatabaseCoordinates,
        database_name: str,
        collection: str,
        filename: str) -> None:
    chunks = pd.read_csv(filename, chunksize=CHUNKSIZE)

    for chunk in chunks:
        cleaned = clean(chunk)
        database.load(coords, database_name, collection, cleaned)
