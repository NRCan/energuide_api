import io
from http import HTTPStatus
import pytest
from extract_endpoint import endpoint_triggers, endpoint, azure_utils


def test_mock_upload_trigger(sample_zipfile: io.BytesIO, sample_timestamp: str):

    mock_upload = endpoint_triggers.MockUploadToAzure(sample_zipfile, sample_timestamp, endpoint.TIMESTAMP_FILENAME)
    result = mock_upload.run()

    assert result == HTTPStatus.CREATED


def test_mock_upload_trigger_bad_file(sample_nonzipfile: io.BytesIO, sample_timestamp: str):

    mock_upload = endpoint_triggers.MockUploadToAzure(sample_nonzipfile, sample_timestamp, endpoint.TIMESTAMP_FILENAME)
    result = mock_upload.run()

    assert result == HTTPStatus.BAD_REQUEST


@pytest.mark.usefixtures('azure_service')
def test_azure_upload_trigger(azure_emulator_coords:
                              azure_utils.StorageCoordinates,
                              sample_zipfile: io.BytesIO,
                              sample_timestamp: str):

    azure_upload = endpoint_triggers.UploadFilesToAzure(sample_zipfile,
                                                        sample_timestamp,
                                                        endpoint.TIMESTAMP_FILENAME,
                                                        azure_emulator_coords)
    result = azure_upload.run()

    assert result == HTTPStatus.CREATED


@pytest.mark.usefixtures('azure_service')
def test_azure_upload_trigger_bad_file(azure_emulator_coords: azure_utils.StorageCoordinates,
                                       sample_nonzipfile: io.BytesIO,
                                       sample_timestamp: str):

    azure_upload = endpoint_triggers.UploadFilesToAzure(sample_nonzipfile,
                                                        sample_timestamp,
                                                        endpoint.TIMESTAMP_FILENAME,
                                                        azure_emulator_coords)
    result = azure_upload.run()

    assert result == HTTPStatus.BAD_REQUEST
