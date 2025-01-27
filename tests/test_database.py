"""
tests/test_database.py


ueats CLI database test
"""

import json
from subprocess import check_output
from .utils import run_and_check
from pathlib import Path


def proccess_json_output(text: str):
    text_dict = json.loads(text)
    status = text_dict["status"]
    output = text_dict["output"]
    error = text_dict["error"]
    return status, output, error


def test_database_setup():
    db_setup_res = check_output(["ueats", "database", "setup"], text=True)
    status, output, error = proccess_json_output(db_setup_res)
    assert status == 0, f"Got an unexpected status - {status}"
    assert not error, f"Got error setting up database - {error}"
    assert "Tables created successfully" in output, "Output did not contain 'successfully' string"
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists(), ""
    db_list_res = check_output(["ueats", "database", "list"], text=True)
    status, output, error = proccess_json_output(db_list_res)
    assert status == 0 and not error, f"Got error listing database\nError: {error}"
    output_tables = list(output.keys())
    expected_tables = ["users", "restaurants", "menus", "orders", "deliveries"]
    for table in output_tables:
        assert table in expected_tables

def test_database_teardown():
    # Check command runs successfully
    run_and_check("ueats database teardown")
    # Check expected file still exists
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    # Verify tables are empty database list
    output = run_and_check("ueats database list")
    assert all(not x for x in output.values())
