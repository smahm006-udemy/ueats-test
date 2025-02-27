import pytest
from .utils import run_and_check, UeatsCommandError


@pytest.mark.order
class TestOrders:
    user = {"name": "Annie", "address": "London"}
    restaurant = {
        "name": "Chilis",
        "address": "Paris",
        "menu": [
            {
                "name": "'Boneless Wings'",
                "count": 10,
                "price": 15,
                "preparation_time": 5,
            }
        ],
    }

    @pytest.mark.parametrize(
        "balance, error_message",
        [
            pytest.param(100, "", marks=[pytest.mark.happy]),
            pytest.param(0, "Insufficient user balance", marks=[pytest.mark.rainy]),
        ],
    )
    def test_order_place(self, setup_tables, balance, error_message):
        item = self.restaurant["menu"][0]
        self.user["wallet"] = balance
        setup_tables(user=self.user, restaurant=self.restaurant)
        if error_message:
            with pytest.raises(UeatsCommandError, match=error_message):
                run_and_check(
                    f"ueats order place {self.user['name']} {self.restaurant['name']} {item['name']}"
                )
        else:
            run_and_check(
                f"ueats order place {self.user['name']} {self.restaurant['name']} {item['name']}"
            )
            result = run_and_check("ueats database list -t users menus orders")
            assert result["orders"][0]["order_status"] == "placed"
            assert (
                result["users"][0]["user_wallet"]
                == balance - result["menus"][0]["item_price"]
            )
