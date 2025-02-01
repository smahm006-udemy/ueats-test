import pytest
from .utils import logger, proccess_json_output, run_and_check


@pytest.mark.user
class TestUsers:
    user_name = "Alice"
    user_address = "Kingston"

    @pytest.mark.happy
    def test_user_add(self):
        run_and_check("ueats user add Alice Kingston")

    def test_user_remove(self):
        pass
