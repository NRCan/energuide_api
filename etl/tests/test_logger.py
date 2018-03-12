import pytest
from energuide import logger


def test_unwrap_exception_message() -> None:
    try:
        try:
            1/0
        except ZeroDivisionError as exc:
            raise ValueError('ValueError Message') from exc
    except ValueError as exc:
        assert logger.unwrap_exception_message(exc, ' - ') == 'ValueError Message - division by zero'
