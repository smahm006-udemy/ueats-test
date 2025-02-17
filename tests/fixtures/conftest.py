import pytest
import urllib.request
import json
from .test_fixtures import logger
from .fixtures import imported

@pytest.fixture
def hello_world():
    """Returns the string Hello, World"""
    return "Hello, World!"


@pytest.fixture
def bitcoin_rate():
    """Return current bitcoin rate, skip test if rate < $60k USD"""
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                pytest.fail("Failed to fetch Bitcoin rate")
            data = json.loads(response.read().decode())
            rate = data["bpi"]["USD"]["rate_float"]
            logger.debug(f"Current Bitcoin rate: ${rate}")
            # Check if the rate is greater than $60,000
            if rate < 60000:
                pytest.skip(f"Bitcoin rate is below $60,000: ${rate}")
            return rate
    except Exception as e:
        pytest.fail(f"Error fetching Bitcoin rate: {e}")


@pytest.fixture
def circle():
    return {"radius": 5}


@pytest.fixture
def circle_area(circle):
    return 3.14 * (circle["radius"] ** 2)


@pytest.fixture
def open_file():
    """Creates and yields a file and closes it during teardown"""
    file_name = "hello_world.txt"
    logger.info(f"Opening file {file_name}")
    file = open(file_name, "w+")
    yield file
    logger.info(f"Closing file {file_name}")
    file.close()


@pytest.fixture
def whereami():
    return "Fixture from local conftest.py inside tests/fixtures folder"
