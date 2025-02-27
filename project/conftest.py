import pytest
import re
from pathlib import Path
from typing import Optional, Dict
from .utils import logger, run_and_check, UeatsCommandError

ueats_file = Path.cwd() / "ueats.db"


@pytest.fixture(scope="session")
def create_database():
    logger.info("Setting up new database")
    run_and_check("ueats database setup")
    yield
    logger.info(f"Deleting database file {ueats_file}")
    ueats_file.unlink()


@pytest.fixture(scope="function", autouse=True)
def teardown_database(create_database):
    logger.info("Tearing down database")
    run_and_check("ueats database teardown")


@pytest.fixture
def setup_tables():
    def setup_tables_inner(user: Optional[Dict], restaurant: Optional[Dict]):
        if user:
            run_and_check(f"ueats user add {user['name']} {user['address']}")
            if "wallet" in user:
                run_and_check(f"ueats wallet deposit {user['name']} {user['wallet']}")
        if restaurant:
            run_and_check(
                f"ueats restaurant add {restaurant['name']} {restaurant['address']}"
            )
            if "menu" in restaurant:
                for item in restaurant["menu"]:
                    run_and_check(
                        f"ueats menu add {restaurant['name']} {item['name']} {item['price']} {item['count']} {item['preparation_time']}"
                    )
    return setup_tables_inner

@pytest.fixture
def place_order():
    def place_order_inner(user_name: str, restaurant_name: str, item_name: str):
        result = run_and_check(
            f"ueats order place {user_name} {restaurant_name} {item_name}"
        )
        order_id = re.findall(r"Order ID: (\d+)", result)
        if not order_id:
            raise ValueError(f"Order ID not found in command output.\nOutput {result}")
        return order_id[0]
    return place_order_inner
