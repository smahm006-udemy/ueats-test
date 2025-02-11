import pytest
import logging

@pytest.fixture
def imported():
    return "Fixture from local fixtures.py inside tests/fixtures folder"


@pytest.fixture(scope="session")
def scoped_fixture():
    x = [0]
    logging.info("Setting up fixture with a function scope")
    yield x
    logging.info("Tearing down fixture with a function scope")
