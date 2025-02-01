"""
tests/utils.py

Utilities to help during testing
"""

import subprocess
import shlex
import json
import logging


def proccess_json_output(text: str):
    text_dict = json.loads(text)
    status = text_dict["status"]
    result = text_dict["result"]
    error = text_dict["error"]
    return status, result, error


def run_and_check(command: str, expected_status: int = 0, expected_error: str = ""):
    logging.debug(f"Running command - \"{command}\"")
    command_list = shlex.split(command)
    result = subprocess.check_output(
        command_list,
        shell=False,
        text=True,
    )
    status, result, error = proccess_json_output(result.strip())
    assert status == expected_status and error == expected_error, f"Got error running command {command}\nStatus:{status}\nError: {error}"
    return result
