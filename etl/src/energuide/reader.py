import os
import itertools
import json
import typing
import zipfile
from azure.storage import blob

InputData = typing.Dict[str, typing.Any]


AZURE_STORAGE_ACCOUNT = os.environ.get('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', '')
AZURE_STORAGE_KEY = os.environ.get('EXTRACT_ENDPOINT_STORAGE_KEY', '')
AZURE_STORAGE_CONTAINER = os.environ.get('EXTRACT_ENDPOINT_CONTAINER', '')
AZURE_STORAGE_DOMAIN = os.environ.get('EXTRACT_ENDPOINT_STORAGE_DOMAIN', None)


def read(filename: str) -> typing.Iterator[InputData]:
    with zipfile.ZipFile(filename) as zip_input:
        files = zip_input.namelist()
        for file in files:
            house = json.loads(zip_input.read(file))
            house['jsonFileName'] = file
            yield house


def read_from_azure() -> typing.Iterator[InputData]:
    azure_service = blob.BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT,
                                          account_key=AZURE_STORAGE_KEY,
                                          custom_domain=AZURE_STORAGE_DOMAIN)
    files = [blob.name for blob in azure_service.list_blobs(AZURE_STORAGE_CONTAINER)]
    for file in files:
        content = azure_service. get_blob_to_bytes(AZURE_STORAGE_CONTAINER, file).content
        house = json.loads(content)
        house['jsonFileName'] = file
        yield house


def grouper(raw: typing.Iterable[InputData],
            grouping_field: str) -> typing.Iterator[typing.List[InputData]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
