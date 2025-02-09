import pytest
import logging

@pytest.fixture
def my_location():
    return "Fixture from module test_fixture_order.py"

class TestFixtureOrder:
    @pytest.fixture
    def my_location(self):
        return "Fixture from module test_fixture_order.py"

    def test_fixture_order(self, my_location, subtests_specific):
        logging.info(my_location)

@pytest.mark.fixture
def test_fixture_scope_session(scoped_fixture):
    scoped_fixture[0] += 1
    logging.debug(f"VALUE = {scoped_fixture}")
