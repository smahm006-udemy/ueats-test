import pytest
import os
import tempfile
from .test_fixtures import logger


@pytest.fixture
def int_list():
    return [150, 140]


@pytest.fixture(autouse=True)
def add_int(int_list):
    int_list.append(130)


# @pytest.mark.usefixtures("cleandir")
@pytest.mark.fixture
class TestAutoFixture:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

    def test_int_list(self, int_list):
        assert len(int_list) == 3
