import pytest
import logging


logger = logging.getLogger("fixture_logger")

@pytest.mark.fixture
class TestFixtures:
    def test_basic_fixture(self, hello_world):
        assert hello_world == "Hello, World!"

    def test_bitcoin_rate(self, bitcoin_rate):
        assert bitcoin_rate > 60000

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
