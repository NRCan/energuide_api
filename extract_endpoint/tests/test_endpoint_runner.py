import io
import typing
from http import HTTPStatus
import pytest
from extract_endpoint import endpoint
from extract_endpoint.endpoint_triggers import EndpointTrigger, MockUploadToAzure, MockTriggerTL
from extract_endpoint.endpoint_runner import EndpointRunner


@pytest.fixture
def sample_trigger_list(sample_zipfile: io.BytesIO,
                        sample_timestamp: str) -> typing.List[EndpointTrigger]:

    sample_trigger_list = [MockUploadToAzure(sample_zipfile, sample_timestamp, endpoint.TIMESTAMP_FILENAME),
                           MockTriggerTL()]

    return sample_trigger_list


@pytest.fixture
def sample_trigger_list_fail(sample_nonzipfile: io.BytesIO, sample_timestamp: str) -> typing.List[EndpointTrigger]:

    sample_trigger_list_fail = [MockUploadToAzure(sample_nonzipfile, sample_timestamp, endpoint.TIMESTAMP_FILENAME),
                                MockTriggerTL()]
    return sample_trigger_list_fail


def test_endpoint_runner_runs_triggers(sample_trigger_list: typing.List[EndpointTrigger]) -> None:
    test_runner = EndpointRunner(sample_trigger_list)
    result = test_runner.apply()
    assert result == HTTPStatus.CREATED
    for trigger in test_runner.triggers:
        assert trigger.run_count == 1


def test_endpoint_runner_stops_if_fail(sample_trigger_list_fail: typing.List[EndpointTrigger]) -> None:
    test_runner = EndpointRunner(sample_trigger_list_fail)
    result = test_runner.apply()
    assert result == HTTPStatus.BAD_REQUEST
    assert test_runner.triggers[0].run_count == 1
    assert test_runner.triggers[1].run_count == 0
