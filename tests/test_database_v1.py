"""
tests/test_database.py


ueats CLI database tests
"""

from typing import Dict
from .utils import run_and_check
from pathlib import Path


def test_database_setup():
    # Check command runs successfully
    output = run_and_check("ueats database setup")
    assert "successfully" in output, "Output did not contain 'successfully' string"
    # Check expected file exists
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    # Verify tables show up in database list
    output: Dict = run_and_check("ueats database list")
    output_tables = list(output.keys())
    expected_tables = ["users", "restaurants", "menus", "orders", "deliveries"]
    assert all(x in output_tables for x in expected_tables)
    assert set(expected_tables).issubset(output_tables)

def test_database_teardown():
    run_and_check("ueats database teardown")
    # Check expected file still exists
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    # Verify tables are empty database list
    output: Dict = run_and_check("ueats database list")
    assert all(not x for x in output.values())
