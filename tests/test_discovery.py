"""
tests/test_discovery.py


Pytest discovery example
"""

import pytest


@pytest.mark.discovery
class TestDiscovery:
    @pytest.mark.basic
    def test_discover_one(self):
        pass

    def test_discover_two(self):
        pass
