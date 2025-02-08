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
