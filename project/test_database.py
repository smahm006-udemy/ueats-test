"""
tests/test_database.py


ueats CLI database test
"""

import pytest
from subprocess import check_output
from .utils import proccess_json_output, run_and_check
from pathlib import Path


@pytest.mark.database()
def test_database_setup():
    db_setup_res = check_output(["ueats", "database", "setup"], text=True)
    status, result, error = proccess_json_output(db_setup_res)
    assert status == 0, f"Got an unexpected status - {status}"
    assert not error, f"Got error setting up database - {error}"
    assert (
        "Tables created successfully" in result
    ), "Result did not contain 'successfully' string"
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists(), ""
    db_list_res = check_output(["ueats", "database", "list"], text=True)
    status, result, error = proccess_json_output(db_list_res)
    assert status == 0 and not error, f"Got error listing database\nStatus:{status}\nError: {error}"
    recieved_tables = list(result.keys())
    expected_tables = ["users", "restaurants", "menus", "orders", "deliveries"]
    for table in recieved_tables:
        assert table in expected_tables


@pytest.mark.database()
def test_database_teardown():
    run_and_check("ueats database teardown")
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    output = run_and_check("ueats database list")
    assert all(not x for x in output.values())
