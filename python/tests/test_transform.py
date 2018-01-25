import pandas as pd
import numpy as np
import pymongo
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
