import pytest
from pathlib import Path
from .utils import UeatsCommandError, logger, run_and_check


@pytest.mark.wallet
class TestWallet:
    user_name = "Bob"
    user_address = "Malibu"
    user_amount = 50
    ueats_file = Path.cwd() / "ueats.db"

    @pytest.mark.happy
    def test_wallet_deposit(self):
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            run_and_check(f"ueats wallet deposit {self.user_name} {self.user_amount}")
            result = run_and_check("ueats database list -t users")
            assert result["users"][0]["wallet"] == self.user_amount
        finally:
            self.ueats_file.unlink()

    @pytest.mark.happy
    def test_wallet_withdraw(self):
        half_amount = self.user_amount // 2
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            run_and_check(f"ueats wallet deposit {self.user_name} {self.user_amount}")
            run_and_check(f"ueats wallet withdraw {self.user_name} {half_amount}")
            result = run_and_check("ueats database list -t users")
            assert result["users"][0]["wallet"] == half_amount
        finally:
            self.ueats_file.unlink()

    @pytest.mark.rainy
    def test_wallet_insufficient_widthdraw(self):
        double_amount = self.user_amount * 2
        try:
            run_and_check("ueats database setup")
            run_and_check(f"ueats user add {self.user_name} {self.user_address}")
            run_and_check(f"ueats wallet deposit {self.user_name} {self.user_amount}")
            with pytest.raises(UeatsCommandError, match="Insufficient balance"):
                run_and_check(f"ueats wallet withdraw {self.user_name} {double_amount}")
        finally:
            self.ueats_file.unlink()
