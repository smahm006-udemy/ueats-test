import pytest
from pathlib import Path
from .utils import logger, run_and_check, UeatsCommandError


@pytest.mark.user
class TestUsers:
    user_name = "Alice"
    user_address = "Kingston"
    ueats_file = Path.cwd() / "ueats.db"

    @pytest.mark.happy
    def test_user_add(self):
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            result = run_and_check("ueats database list -t users")
            for user in result["users"]:
                if user["user_name"] == self.user_name:
                    assert user["user_address"] == self.user_address
                    break
            else:
                logger.error(f'Users list :- {result["users"]}')
                raise ValueError(f"{self.user_name} not found in any users")
        finally:
            self.ueats_file.unlink()

    @pytest.mark.rainy
    def test_user_duplicate(self):
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            with pytest.raises(
                UeatsCommandError, match=f"User '{self.user_name}' already exists"
            ):
                run_and_check(f"ueats user add {self.user_name} {self.user_address}")
        finally:
            self.ueats_file.unlink()

    @pytest.mark.happy
    def test_user_remove(self):
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            run_and_check(f"ueats user remove {self.user_name}")
            result = run_and_check("ueats database list -t users")
            assert all(self.user_name not in x["user_name"] for x in result["users"])
        finally:
            self.ueats_file.unlink()
