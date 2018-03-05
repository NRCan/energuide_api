import os
import itertools
import json
import typing
import zipfile
from azure.storage import blob


def read(filename: str) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    with zipfile.ZipFile(filename) as zip_input:
        files = zip_input.namelist()
        for file in files:
            house = json.loads(zip_input.read(file))
            house['jsonFileName'] = file
            yield house


def read_from_azure() -> typing.Iterator[typing.Dict[str, typing.Any]]:
    account = os.environ.get('EXTRACT_ENDPOINT_STORAGE_ACCOUNT', '')
    key = os.environ.get('EXTRACT_ENDPOINT_STORAGE_KEY', '')
    container = os.environ.get('EXTRACT_ENDPOINT_CONTAINER', '')
    domain = os.environ.get('EXTRACT_ENDPOINT_STORAGE_DOMAIN', None)

    azure_service = blob.BlockBlobService(account_name=account,
                                          account_key=key,
                                          custom_domain=domain)
    # itertools.groupby() needs its input sorted by the groupby key. We are assuming that that key is the filename
    files = sorted([blob_.name for blob_ in azure_service.list_blobs(container)
                    if 'timestamp' not in blob_.name])
    for file in files:
        content = azure_service. get_blob_to_bytes(container, file).content
        house = json.loads(content)
        house['jsonFileName'] = file
        yield house


def grouper(raw: typing.Iterable[typing.Dict[str, typing.Any]],
            grouping_field: str) -> typing.Iterator[typing.List[typing.Dict[str, typing.Any]]]:

    for group in itertools.groupby(raw, lambda y: y.get(grouping_field)):
        yield [x for x in group[1]]
