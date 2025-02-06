import pytest
import urllib.request
import json
import logging


@pytest.fixture
def hello_world():
    return "Hello, World!"


@pytest.fixture
def bitcoin_rate():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                pytest.fail("Failed to fetch Bitcoin rate")
            data = json.loads(response.read().decode())
            rate = data["bpi"]["USD"]["rate_float"]
            logging.debug(f"Current Bitcoin rate: ${rate}")
            # Check if the rate is greater than $60,000
            if rate < 60000:
                pytest.skip(f"Bitcoin rate is below $60,000: ${rate}")
            return rate
    except Exception as e:
        pytest.fail(f"Error fetching Bitcoin rate: {e}")


@pytest.fixture
def open_file():
    file_name = "hello_world.txt"
    logging.info(f"Opening file {file_name}")
    file = open(file_name, "w+")
    yield file
    logging.info(f"Closing file {file_name}")
    file.close()


# @pytest.fixture
# def open_file(request):
#     file_name = "hello_world.txt"
#     logging.info(f"Opening file {file_name}")
#     file = open(file_name, "w+")

#     def close_file():
#         logging.info(f"Closing file {file_name}")
#         file.close()

#     request.addfinalizer(close_file)
#     return file


@pytest.mark.fixture
class TestFixtures:
    def test_basic_fixture(self, hello_world):
        assert hello_world == "Hello, World!"

    def test_bitcoin_rate(self, bitcoin_rate):
        assert bitcoin_rate > 60000

    def test_write_to_file(self, hello_world, open_file):
        logging.info(f"Writing '{hello_world}' to file")
        open_file.write(hello_world)
        open_file.flush()
        open_file.seek(0)
        written_content = open_file.read()
        logging.debug(f"File read contents: '{written_content}'")
        assert written_content == hello_world, (
            f"Expected '{hello_world}', but got '{written_content}'"
        )
