"""
tests/test_exceptions.py


Test stuff with exceptions.
"""

import sys
import pytest
import logging

if not sys.platform.startswith("linux"):
    pytest.skip(reason="Only Linux PC's can run these tests", allow_module_level=True)


class CustomError(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        if self.code >= 100:
            return f"Major Error {self.code}: {self.message}"
        else:
            return f"Minor Error {self.code}: {self.message}"


@pytest.mark.exception
class TestException:
    def test_pytest_raises(self):
        with pytest.raises(AssertionError, match="One plus one is two") as execinfo:
            assert 1 + 1 == 3, "One plus one is two"
        logging.debug(f"Exception Type: {execinfo.type}")
        logging.debug(f"Exception Value: {execinfo.value}")
        logging.debug(f"Exception Traceback: {execinfo.traceback}")

    def test_try_except_else(self):
        try:
            x = 1 / 0
        except ZeroDivisionError as zde:
            logging.info(f"ZeroDivisionError error caught - {zde}")
            try:
                assert 1 + 1 == 3
            except AssertionError as ae:
                logging.info(f"Assertion error caught - {ae}")
        else:
            logging.error("No Exceptions caught")
            raise OSError("No Exceptions caught")
        finally:
            logging.info("Test Ended")

    def test_custom_exception(self):
        with pytest.raises(CustomError, match=r"Minor Error \d+: Custom error.*"):
            raise CustomError("Custom error string", 20)
        with pytest.raises(CustomError, match=r"Major Error \d+: Custom error.*"):
            raise CustomError("Custom error string", 100)


class TestSkip:
    @pytest.mark.skip(reason="Not complete yet")
    def test_incomplete_skip(self):
        logging.warning("Test needs more time to finish")

    @pytest.mark.skipif(
        sys.version_info < (3, 10), reason="requires python3.10 or higher"
    )
    def test_invalid_version_skip(self):
        x = "A"
        match x:
            case "A":
                print("matched A")
            case _:
                print("No match")

    def test_invalid_configuration_skif(self):
        try:
            file = open("random")
        except FileNotFoundError:
            pytest.skip(reason="Configuration file not found")


class TestXfail:
    @pytest.mark.xfail(reason="Bug in win32 libraries")
    def test_bug_xfail(self):
        assert False

    def test_slow_request_xfail(self):
        import http.client

        conn = http.client.HTTPConnection("10.255.255.1", timeout=5)
        try:
            conn.request("GET", "/")
            conn.getresponse()
        except OSError:
            pytest.xfail(f"Server did not respond in time...")
        finally:
            conn.close()
