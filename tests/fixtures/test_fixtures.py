import pytest
import logging
from .fixtures import scoped_fixture


logger = logging.getLogger("fixture_logger")


@pytest.mark.fixture
def test_fixture_scope_module(scoped_fixture):
    scoped_fixture[0] += 1
    logger.debug(f"VALUE = {scoped_fixture}")


@pytest.fixture
def my_location():
    return "Fixture from module test_fixtures.py"


@pytest.mark.fixture
class TestFixtures:
    @pytest.fixture
    def my_location(self):
        return "Fixture from class TestFixtures inside test_fixtures.py"

    def test_basic_fixture(self, hello_world):
        assert hello_world == "Hello, World!"

    def test_bitcoin_rate(self, bitcoin_rate):
        assert bitcoin_rate > 60000

    def test_circle_area(self, circle_area):
        assert int(circle_area) == 78

    def test_write_to_file(self, hello_world, open_file):
        logger.info(f"Writing '{hello_world}' to file")
        open_file.write(hello_world)
        open_file.flush()
        open_file.seek(0)
        written_content = open_file.read()
        logger.debug(f"File read contents: '{written_content}'")
        assert written_content == hello_world, (
            f"Expected '{hello_world}', but got '{written_content}'"
        )

    def test_fixture_order(self, imported):
        logging.info(imported)

    def test_fixture_scope_function(self, scoped_fixture):
        scoped_fixture[0] += 1
        logger.debug(f"NEW VALUE = {scoped_fixture}")

    def test_fixture_scope_class(self, scoped_fixture):
        scoped_fixture[0] += 1
        logger.debug(f"NEW VALUE = {scoped_fixture}")
