import pytest
from pathlib import Path
from .utils import logger, proccess_json_output, run_and_check, UeatsCommandError


@pytest.mark.menu
class TestMenu:
    restaurant_name = "McDonalds"
    restaurant_address = "Dallas"
    item_name = "BigMac"
    item_price = 15
    item_count = 50
    item_preptime = 5

    @pytest.fixture
    def restaurant(self):
        logger.info(f"Adding restaurant {self.restaurant_name}")
        run_and_check(
            f"ueats restaurant add {self.restaurant_name} {self.restaurant_address}"
        )
        yield
        logger.info(f"Removing restaurant {self.restaurant_name}")
        run_and_check(f"ueats restaurant remove {self.restaurant_name}")

    @pytest.mark.happy
    def test_menu_add(self, database, restaurant):
        run_and_check(
            f"ueats menu add {self.restaurant_name} {self.item_name} {self.item_price} {self.item_count} {self.item_preptime}"
        )
        result = run_and_check("ueats database list -t restaurants menus")
        restaurant_id = 0
        for restaurant in result["restaurants"]:
            if restaurant["restaurant_name"] == self.restaurant_name:
                restaurant_id = restaurant["id"]
                break
        assert restaurant_id, (
            f"No restaurant named {self.restaurant_name} found in database"
        )
        for menu in result["menus"]:
            if menu["restaurant_id"] == restaurant_id:
                assert menu["item_name"] == self.item_name
                assert menu["item_price"] == self.item_price
                assert menu["item_count"] == self.item_count
                assert menu["item_preparation_time"] == self.item_preptime
                break
        else:
            logger.error(f"Menus list :- {result['menus']}")
            raise ValueError(
                f"No menu items found for restaurant {self.restaurant_name}"
            )

    @pytest.mark.happy
    def test_menu_invalid_preptime(self, database, restaurant):
        self.item_preptime = 11
        with pytest.raises(UeatsCommandError):
            run_and_check(
                f"ueats menu add {self.restaurant_name} {self.item_name} {self.item_price} {self.item_count} {self.item_preptime}"
            )

    @pytest.mark.happy
    def test_menu_update(self, database, restaurant):
        run_and_check(
            f"ueats menu add {self.restaurant_name} {self.item_name} {self.item_price} {self.item_count} {self.item_preptime}"
        )
        new_item_price = self.item_price + 10
        run_and_check(
            f"ueats menu update {self.restaurant_name} {self.item_name} {new_item_price} {self.item_count} {self.item_preptime}"
        )
        restaurant_id = 0
        result = run_and_check("ueats database list -t restaurants menus")
        for restaurant in result["restaurants"]:
            if restaurant["restaurant_name"] == self.restaurant_name:
                restaurant_id = restaurant["id"]
                break
        assert restaurant_id, (
            f"No restaurant named {self.restaurant_name} found in database"
        )
        for menu in result["menus"]:
            if menu["restaurant_id"] == restaurant_id:
                assert menu["item_name"] == self.item_name
                assert menu["item_price"] == new_item_price
                assert menu["item_count"] == self.item_count
                assert menu["item_preparation_time"] == self.item_preptime
                break
        else:
            logger.error(f"Menus list :- {result['menus']}")
            raise ValueError(
                f"No menu items found for restaurant {self.restaurant_name}"
            )


    @pytest.mark.happy
    def test_menu_remove(self, database, restaurant):
        run_and_check(
            f"ueats menu add {self.restaurant_name} {self.item_name} {self.item_price} {self.item_count} {self.item_preptime}"
        )
        run_and_check(f"ueats menu remove {self.restaurant_name} {self.item_name}")
        result = run_and_check("ueats database list -t menus")
        assert all(self.item_name not in x["item_name"] for x in result["menus"])
