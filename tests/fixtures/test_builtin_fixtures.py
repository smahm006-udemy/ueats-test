import pytest
from pathlib import Path
from subprocess import run
from .test_fixtures import logger
import time


@pytest.fixture
def expensive_ten(cache):
    """Simulates an expensive operation by sleeping."""
    result = cache.get("key", None)
    if not result:
        time.sleep(2)  # Simulate a delay of 2 seconds
        result = 10
        cache.set("key", result)
    return result


@pytest.mark.fixture
class TestBuiltinFixture:
    def test_request_fixture(self, request: pytest.FixtureRequest):
        logger.info(f"Test node id: {request.node.nodeid}")
        logger.info(f"Test full path: {request.path}")
        if request.config.getoption("verbose") > 1:
            logger.debug(f"Verbose level high")

    def test_tmp_path_fixture(self, tmp_path: Path):
        file = tmp_path / "example.txt"
        logger.info(f"Writing to file: {file.absolute()}")
        _ = file.write_text("Hello, pytest!")
        assert file.read_text() == "Hello, pytest!"

    def test_tmp_path_factory_fixture(self, tmp_path_factory: pytest.TempPathFactory):
        path: Path = tmp_path_factory.mktemp(basename="test")
        file = path / "example.txt"
        logger.info(f"Writing to file: {file.absolute()}")
        _ = file.write_text("Hello, pytest!")
        assert file.read_text() == "Hello, pytest!"

    def test_capsys_fixture(self, capsys: pytest.CaptureFixture[str]):
        run("echo Hello", shell=True)
        print("World")
        logger.info(capsys.readouterr())

    def test_capfd_fixture(self, capfd: pytest.CaptureFixture[str]):
        run("echo Hello", shell=True)
        print("World")
        logger.info(capfd.readouterr())

    def test_caplog_fixture(self, caplog: pytest.LogCaptureFixture):
        logger.warning("Hello")
        logger.debug("World")
        logger.info(caplog.messages)

    def test_caplog_fixture(self, caplog: pytest.LogCaptureFixture):
        logger.warning("Hello")
        logger.debug("World")
        logger.info(caplog.messages)

    @pytest.mark.parametrize("value, expected", [(1, 10), (2, 20), (3, 30)])
    def test_cache_fixture(self, expensive_ten, value, expected):
        assert expensive_ten * value == expected
