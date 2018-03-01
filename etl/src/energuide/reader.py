import os
import itertools
import json
import typing
import zipfile
from azure.storage import blob

InputData = typing.Dict[str, typing.Any]


EXTRACT_ENDPOINT_STORAGE_ACCOUNT = os.environ.get('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', '')
EXTRACT_ENDPOINT_STORAGE_KEY = os.environ.get('EXTRACT_ENDPOINT_STORAGE_KEY', '')
EXTRACT_ENDPOINT_CONTAINER = os.environ.get('EXTRACT_ENDPOINT_CONTAINER', '')
EXTRACT_ENDPOINT_STORAGE_DOMAIN = os.environ.get('EXTRACT_ENDPOINT_STORAGE_DOMAIN', None)


def read(filename: str) -> typing.Iterator[InputData]:
    with zipfile.ZipFile(filename) as zip_input:
        files = zip_input.namelist()
        for file in files:
            house = json.loads(zip_input.read(file))
            house['jsonFileName'] = file
            yield house


def read_from_azure() -> typing.Iterator[InputData]:

    azure_service = blob.BlockBlobService(account_name=EXTRACT_ENDPOINT_STORAGE_ACCOUNT,
                                          account_key=EXTRACT_ENDPOINT_STORAGE_KEY,
                                          custom_domain=EXTRACT_ENDPOINT_STORAGE_DOMAIN)
    # itertools.groupby() needs its input sorted by the groupby key. We are assuming that that key is the filename
    files = sorted([blob.name for blob in azure_service.list_blobs(EXTRACT_ENDPOINT_CONTAINER)])
    for file in files:
        content = azure_service. get_blob_to_bytes(EXTRACT_ENDPOINT_CONTAINER, file).content
        house = json.loads(content)
        house['jsonFileName'] = file
        yield house


def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
