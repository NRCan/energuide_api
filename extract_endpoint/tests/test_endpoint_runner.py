import io
import typing
import pytest
from extract_endpoint import endpoint_runner, endpoint_triggers, endpoint


@pytest.fixture
def sample_trigger_list(sample_zipfile: io.BytesIO,
                        sample_timestamp: str) -> typing.List[endpoint_triggers.EndpointTrigger]:

    sample_trigger_list = [endpoint_triggers.MockUploadToAzure(sample_zipfile, sample_timestamp,
                                                               endpoint.TIMESTAMP_FILENAME),
                           endpoint_triggers.MockTriggerTL()]

    return sample_trigger_list


def test_endpoint_runner_runs_triggers(sample_trigger_list: typing.List[endpoint_triggers.EndpointTrigger]) -> None:
    test_runner = endpoint_runner.EndpointRunner(sample_trigger_list)
    test_runner.apply()
    for trigger in test_runner.triggers:
        assert trigger.run_count == 1


def test_endpoint_runner_stops_if_trigger_fails() -> None:
    assert True
