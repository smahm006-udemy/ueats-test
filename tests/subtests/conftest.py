import pytest
from .subtest_fixtures import subtests_specific

@pytest.fixture
def my_location():
    return "Fixture from local conftest.py inside tests/subtests"
