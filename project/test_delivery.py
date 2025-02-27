import pytest
import re
import time
from pytest_mock import MockFixture
from project.utils import logger, run_and_check, UeatsCommandError


@pytest.mark.delivery
class TestDelivery:
    user = {"name": "Annie", "address": "London", "wallet": 100}
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

    @pytest.mark.restaurant
    @pytest.mark.happy
    def test_restaurant_prepare(self, setup_tables, place_order):
        item = self.restaurant["menu"][0]
        setup_tables(user=self.user, restaurant=self.restaurant)
        order_id = place_order(self.user["name"], self.restaurant["name"], item["name"])
        start = time.monotonic()
        run_and_check(f"ueats restaurant prepare {self.restaurant['name']} {order_id}")
        time_elapased = int(time.monotonic() - start)
        logger.debug(f"Time taken to prepare item - {time_elapased} seconds")
        assert time_elapased == item["preparation_time"]
        result = run_and_check("ueats database list -t orders")
        assert result["orders"][0]["order_status"] == "prepared"

    @pytest.mark.happy
    def test_delivery_time(self, setup_tables):
        setup_tables(user=self.user, restaurant=self.restaurant)
        for _ in range(10):
            result = run_and_check(
                f"ueats delivery time {self.user['name']} {self.restaurant['name']}"
            )
            time = re.findall(r".* (\d+) seconds", result)
            assert time and (int(time[0]) > 0 and int(time[0]) <= 10)

    @pytest.mark.happy
    def test_delivery_start(self, mocker: MockFixture, setup_tables, place_order):
        item = self.restaurant["menu"][0]
        setup_tables(user=self.user, restaurant=self.restaurant)
        order_id = place_order(self.user["name"], self.restaurant["name"], item["name"])
        run_and_check(f"ueats restaurant prepare {self.restaurant['name']} {order_id}")
        mock_time = mocker.patch(f"{__name__}.run_and_check", return_value=5)
        delivery_time = run_and_check(
            f"ueats delivery time {self.user['name']} {self.restaurant['name']}"
        )
        logger.debug(f"Mocked delivery time: {delivery_time}")
        mocker.stop(mock_time)
        start = time.monotonic()
        result = run_and_check(f"ueats delivery start {order_id} {delivery_time}")
        time_elapased = int(time.monotonic() - start)
        logger.debug(f"Time taken to deliver item - {time_elapased}")
        assert time_elapased == 5
        result = run_and_check("ueats database list -t restaurants menus orders")
        assert result["orders"][0]["order_status"] == "delivered"
        assert (
            result["restaurants"][0]["restaurant_wallet"]
            == 0 + result["menus"][0]["item_price"]
        )

    @pytest.mark.rainy
    def test_unprepared_delivery(self, mocker: MockFixture, setup_tables, place_order):
        item = self.restaurant["menu"][0]
        setup_tables(user=self.user, restaurant=self.restaurant)
        order_id = place_order(self.user["name"], self.restaurant["name"], item["name"])
        mock_time = mocker.patch(f"{__name__}.run_and_check", return_value=5)
        delivery_time = run_and_check(
            f"ueats delivery time {self.user['name']} {self.restaurant['name']}"
        )
        logger.debug(f"Mocked delivery time: {delivery_time}")
        mocker.stop(mock_time)
        with pytest.raises(
            UeatsCommandError, match="Delivery can only start if order is in"
        ):
            run_and_check(f"ueats delivery start {order_id} {delivery_time}")

    @pytest.mark.happy
    def test_order_cancel(self, setup_tables):
        item = self.restaurant["menu"][0]
        self.user["wallet"] = 100
        setup_tables(user=self.user, restaurant=self.restaurant)
        result = run_and_check(
            f"ueats order place {self.user['name']} {self.restaurant['name']} {item['name']}"
        )
        order_id = re.findall(r"Order ID: (\d+)", result)
        if not order_id:
            raise ValueError(f"Order ID not found in command output.\nOutput {result}")
        run_and_check(f"ueats order cancel {order_id[0]}")
        result = run_and_check("ueats database list -t users orders")
        order_data = result["orders"][0]
        assert order_data["order_status"] == "cancelled"

    @pytest.mark.order
    @pytest.mark.happy
    def test_order_history(self, mocker: MockFixture, setup_tables, place_order):
        def get_order_history():
            result = run_and_check(
                f"ueats order history {self.user['name']} {self.restaurant['name']}"
            )
            logger.debug(result)
            return result["orders"][-1]["status"]

        item = self.restaurant["menu"][0]
        setup_tables(user=self.user, restaurant=self.restaurant)
        # Check status after placing order
        order_id = place_order(self.user["name"], self.restaurant["name"], item["name"])
        status_after_place = get_order_history()
        assert (
            status_after_place == "placed"
        ), f"Expected order ID to be 'placed' but found it in {status_after_place}"
        # Check status after restaurant finished preparing order
        run_and_check(f"ueats restaurant prepare {self.restaurant['name']} {order_id}")
        status_after_prepare = get_order_history()
        assert (
            status_after_prepare == "prepared"
        ), f"Expected order ID to be 'prepared' but found it in {status_after_prepare}"
        # Check status after item has been delivered
        mock_time = mocker.patch(f"{__name__}.run_and_check", return_value=5)
        delivery_time = run_and_check(
            f"ueats delivery time {self.user['name']} {self.restaurant['name']}"
        )
        logger.debug(f"Mocked delivery time: {delivery_time}")
        mocker.stop(mock_time)
        run_and_check(f"ueats delivery start {order_id} {delivery_time}")
        status_after_delivered = get_order_history()
        assert (
            status_after_delivered == "delivered"
        ), f"Expected order ID to be 'delivered' but found it in {status_after_delivered}"
