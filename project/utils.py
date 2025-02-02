"""
tests/utils.py

Utilities to help during testing
"""

import subprocess
import shlex
import json
import logging


logger = logging.getLogger("ueats_logger")

class UeatsCommandError(Exception):
    """Exception raised if running a ueats command returns an error"""

    def __init__(self, status, message):
        self.message = message
        self.status= status

    def __str__(self):
        return f"Status {self.status}, Error: {self.message}"


def proccess_json_output(text: str):
    text_dict = json.loads(text)
    status = text_dict["status"]
    result = text_dict["result"]
    error = text_dict["error"]
    return status, result, error


def run_and_check(command: str):
    logger.debug(f'Running command - "{command}"')
    command_list = shlex.split(command)
    output = subprocess.check_output(
        command_list,
        shell=False,
        text=True,
    )
    status, result, error = proccess_json_output(output.strip())
    if status != 0 or error != "":
        raise UeatsCommandError(status, error)
    return result
