import pytest
from pathlib import Path
from .utils import logger, proccess_json_output, run_and_check, UeatsCommandError


@pytest.mark.restaurant
class TestRestaurants:
    restaurant_name = "McDonalds"
    restaurant_address = "Dallas"

    @pytest.mark.happy
    def test_restaurant_add(self, database):
        run_and_check(
            f"ueats restaurant add {self.restaurant_name} {self.restaurant_address}"
        )
        result = run_and_check("ueats database list -t restaurants")
        for restaurant in result["restaurants"]:
            if restaurant["restaurant_name"] == self.restaurant_name:
                assert restaurant["restaurant_address"] == self.restaurant_address
                break
        else:
            logger.error(f"Restaurants list :- {result['restaurants']}")
            raise ValueError(f"{self.restaurant_name} not found in any restaurants")

    @pytest.mark.rainy
    def test_restaurant_add_duplicate(self, database):
        run_and_check(
            f"ueats restaurant add {self.restaurant_name} {self.restaurant_address}"
        )
        with pytest.raises(
            UeatsCommandError,
            match=f"Restaurant '{self.restaurant_name}' already exists",
        ):
            run_and_check(
                f"ueats restaurant add {self.restaurant_name} {self.restaurant_address}"
            )

    @pytest.mark.happy
    def test_restaurant_remove(self, database):
        run_and_check(f"ueats restaurant add {self.restaurant_name} {self.restaurant_address}")
        run_and_check(f"ueats restaurant remove {self.restaurant_name}")
        result = run_and_check("ueats database list -t restaurants")
        assert all(self.restaurant_name not in x["restaurant_name"] for x in result["restaurants"])


    @pytest.mark.rainy
    def test_restaurant_remove_noexist(self, database):
        with pytest.raises(
            UeatsCommandError,
            match=f"Restaurant '{self.restaurant_name}' does not exist",
        ):
            run_and_check(f"ueats restaurant remove {self.restaurant_name}")
