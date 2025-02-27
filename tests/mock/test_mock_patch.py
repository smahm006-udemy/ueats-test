import pytest
import os
from pytest_mock import MockFixture
from .test_mock_object import User, logger
from .file_utils import read_file, process_lines

print(dir())


@pytest.mark.mock
class TestMockPatch:
    def test_patch(self, class_mocker: MockFixture):
        logger.debug(f"read_file defined in: {read_file.__module__}")
        logger.debug(f"current module: {__name__}")
        # Imports “package.module.object”
        mock_object = class_mocker.patch(
            f"{__name__}.read_file",
            return_value=[
                "INFO: System started",
                "DEBUG: This is a debug message",
                "INFO: User logged in",
                "WARNING: Low disk space",
            ],
        )
        file_lines = read_file("fakefile.txt")
        result = process_lines(file_lines)
        assert result == [file_lines[0], file_lines[2]]

    def test_patch_again(self):
        logger.debug(read_file("faketest.txt"))

    def test_patch_user(self, mocker: MockFixture):
        _ = mocker.patch(f"{__name__}.User", autospec=True)
        user = User()
        logger.debug(user.get_user_name())

    def test_patch_object(self, mocker: MockFixture):
        user = User("Sponge Bob")
        mocked_un = mocker.patch.object(user, 'user_name', 'Whats my name?')
        logger.debug(user.user_name)
        mocker.stop(mocked_un)
        logger.debug(user.user_name)

    def test_monkeypatch(self, monkeypatch):
        class Config:
            log_level = "info"
        monkeypatch.setenv('API_KEY', 'MOCKED_KEY')
        logger.debug(os.getenv('API_KEY'))
        config = Config()
        monkeypatch.setattr(config, "log_level", "error")
        logger.debug(config.log_level)
