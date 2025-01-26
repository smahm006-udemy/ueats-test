"""
tests/utils.py

Utilities to help during testing
"""

import subprocess
import shlex
import json


def proccess_json_output(text: str):
    text_dict = json.loads(text)
    status = text_dict["status"]
    output = text_dict["output"]
    error = text_dict["error"]
    return status, output, error


def run_and_check(command: str):
    command_list = shlex.split(command)
    result = subprocess.check_output(
        command_list,
        shell=False,
        text=True,
    )
    status, output, error = proccess_json_output(result.strip())
    assert status == 0 and not error, f"Got error running command {command} - {error}"
    return output
