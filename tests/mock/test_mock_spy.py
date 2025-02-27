import pytest
import requests
from pytest_mock import MockFixture
from .test_mock_object import User, logger

API_URL = "http://fakeapi.com/weather"


def get_weather_data(retries=1):
    if retries > 5:
        raise AssertionError("get_weather_data failed more than five times!")
    try:
        logger.info("Trying API call")
        requests.get(API_URL)
    except Exception as err:
        get_weather_data(retries=retries + 1)


@pytest.mark.mock
class TestMockSpy:
    def test_get_weather(self, mocker: MockFixture):
        mocked_get = mocker.patch(
            "requests.get", side_effect=Exception("API call failed")
        )
        with pytest.raises(AssertionError):
            get_weather_data()
        logger.debug(mocked_get.mock_calls)
        logger.debug(mocked_get.call_args)
        logger.debug(mocked_get.call_count)
        assert mocked_get.call_count == 5
        logger.debug(mocked_get.assert_called())
        logger.debug(mocked_get.assert_called_with(API_URL))

    def test_spy_caculator(self, mocker: MockFixture):
        class Calculator:
            def add(self, a, b):
                return a + b
        calc = Calculator()
        spy_add = mocker.spy(calc, "add")
        result = calc.add(2, 3)
        spy_add.assert_called_with(2, 3)
        spy_add.assert_called_once()
        assert result == 5
        _ = calc.add(3, 4)
        assert spy_add.call_count == 2
