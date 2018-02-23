import io
import pytest
from azure.storage import blob
from extract_endpoint import azure_utils


@pytest.fixture
def azure_service() -> blob.BlockBlobService:
    azure_service = blob.BlockBlobService(account_name=azure_utils.AZURE_EMULATOR_COORDS.account,
                                          account_key=azure_utils.AZURE_EMULATOR_COORDS.key,
                                          custom_domain=azure_utils.AZURE_EMULATOR_COORDS.domain)
    azure_service.create_container(azure_utils.AZURE_EMULATOR_COORDS.container)
    yield azure_service
    azure_service.delete_container(azure_utils.AZURE_EMULATOR_COORDS.container)


@pytest.fixture
def sample_stream_content() -> str:
    return "Sample stream content"


@pytest.fixture
def sample_stream(sample_stream_content: str) -> io.BytesIO:
    return io.BytesIO(sample_stream_content.encode())


@pytest.fixture
def sample_filename() -> str:
    return "sample_filename.txt"


def test_upload_stream_to_azure(azure_service: blob.BlockBlobService,
                                sample_stream: io.BytesIO,
                                sample_stream_content: str,
                                sample_filename: str) -> None:

    assert azure_utils.upload_stream_to_azure(azure_utils.AZURE_EMULATOR_COORDS, sample_stream, sample_filename)
    assert sample_filename in \
           [blob.name for blob in azure_service.list_blobs(azure_utils.AZURE_EMULATOR_COORDS.container)]
    actual_file_blob = azure_service.get_blob_to_text(azure_utils.AZURE_EMULATOR_COORDS.container, sample_filename)
    assert actual_file_blob.content == sample_stream_content
