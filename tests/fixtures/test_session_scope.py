import pytest
import logging
from .fixtures import scoped_fixture


@pytest.mark.fixture
def test_fixture_scope_session(scoped_fixture):
    scoped_fixture[0] += 1
    logging.debug(f"VALUE = {scoped_fixture}")
