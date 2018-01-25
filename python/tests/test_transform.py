import datetime
import pandas as pd
import numpy as np
import pymongo
import pytest
from energuide import database
from energuide import transform


def test_clean() -> None:
    dataframe = pd.DataFrame.from_dict({'foo': [np.NaN]}, orient='columns')
    output = transform.clean(dataframe).to_dict('records')

    expected = [{'foo': None}]
    assert output == expected


def test_run(database_coordinates: database.DatabaseCoordinates,
             mongo_client: pymongo.MongoClient,
             database_name: str,
             collection: str,
             energuide_fixture: str) -> None:

    transform.run(database_coordinates, database_name, collection, energuide_fixture)
    assert mongo_client[database_name][collection].count() == 3


@pytest.fixture
def sample() -> pd.DataFrame:
    data = {
        'EVAL_ID': 123456,
        'IDNUMBER': 23,
        'CREATIONDATE': '2009-01-01 12:01:02',
        'MODIFICATIONDATE': '2011-01-01 00:01:02',
        'YEARBUILT': 1979,
        'HOUSEREGION': 'Ontario',
        'CLIENTCITY': 'Kingston',
        'CLIENTPCODE': 'K0H 1Y0',
    }
    return pd.DataFrame.from_dict(data)


def test_clean_with_sample(sample: pd.DataFrame) -> None:
    output = transform.clean(sample).to_dict('records')

    expected = {
        'evalId': 123456,
        'idNumber': 23,
        'yearBuilt': 1979,
        'houseRegion': 'Ontario',
        'clientCity': 'Kingston',
        'clientForwardSortationArea': 'K0H',
        'clientPostalCode': 'K0H 1Y0',
        'evaluations': [
            {
                'creationDate': datetime.datetime(2009, 1, 1, 12, 1, 2),
                'modificationDate': datetime.datetime(2011, 1, 1, 0, 1, 2),
            }
        ]
    }
    assert output == expected
