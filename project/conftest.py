import pytest
from pathlib import Path
from .utils import logger, run_and_check

ueats_file = Path.cwd() / "ueats.db"


@pytest.fixture(scope="function")
def create_database():
    logger.info("Setting up new database")
    run_and_check("ueats database setup")
    yield
    logger.info(f"Deleting database file {ueats_file}")
    ueats_file.unlink()
