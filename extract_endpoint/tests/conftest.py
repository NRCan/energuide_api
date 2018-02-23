import pytest
from azure.storage import blob
from extract_endpoint import azure_utils


@pytest.fixture
def azure_emulator_coords() -> azure_utils.StorageCoordinates:
    return azure_utils.StorageCoordinates(
        account='devstoreaccount1',
        key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==',
        container='test-container',
        domain='http://127.0.0.1:10000/devstoreaccount1',
    )


@pytest.fixture
def azure_service(azure_emulator_coords) -> blob.BlockBlobService:
    azure_service = blob.BlockBlobService(account_name=azure_emulator_coords.account,
                                          account_key=azure_emulator_coords.key,
                                          custom_domain=azure_emulator_coords.domain)
    azure_service.create_container(azure_emulator_coords.container)
    yield azure_service
    azure_service.delete_container(azure_emulator_coords.container)
