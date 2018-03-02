import pytest


@pytest.mark.usefixtures('is_azurite_running')
def test_if_azure_is_running():
    assert True
