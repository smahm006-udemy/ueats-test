"""
tests/test_database.py


ueats CLI database test
"""

import json
from subprocess import check_output
from pathlib import Path


def proccess_json_output(text: str):
    text_dict = json.loads(text)
    status = text_dict["status"]
    output = text_dict["output"]
    error = text_dict["error"]
    return status, output, error


def test_database_setup():
    db_setup_res = check_output(f"ueats database setup", shell=True, text=True)
    status, output, error = proccess_json_output(db_setup_res)
    assert status == 0 and not error, f"Got error setting up database\nError: {error}"
    assert "successfully" in output, "Output did not contain 'successfully' string"
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    db_list_res = check_output(f"ueats database list", shell=True, text=True)
    status, output, error = proccess_json_output(db_list_res)
    assert status == 0 and not error, f"Got error listing database\nError: {error}"
    output_tables = list(output.keys())
    expected_tables = ["users", "restaurants", "menus", "orders", "deliveries"]
    assert all(x in output_tables for x in expected_tables)

def test_database_teardown():
    db_teardown_res = check_output(f"ueats database teardown", shell=True, text=True)
    status, _, error = proccess_json_output(db_teardown_res)
    assert status == 0 and not error, f"Got error setting up database\nError: {error}"
    ueats_file = Path.cwd() / "ueats.db"
    assert ueats_file.exists()
    db_list_res = check_output(f"ueats database list", shell=True, text=True)
    status, output, error = proccess_json_output(db_list_res)
    assert status == 0 and not error, f"Got error listing database\nError: {error}"
    assert all(not x for x in output.values())
