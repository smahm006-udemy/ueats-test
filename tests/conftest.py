import pytest

@pytest.fixture
def whereami():
    return "Fixture from parent conftest.py inside tests"
