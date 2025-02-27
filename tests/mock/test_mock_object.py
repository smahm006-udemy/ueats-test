import pytest
from pytest_mock import MockFixture
import logging

logger = logging.getLogger(__name__)


class User:
    def __init__(self, user_name="John") -> None:
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name


def calculate_gpa(api_client, student_name):
    api_url = f"https://fakeapi.com/students/{student_name}/grades"
    response = api_client.get(api_url)
    assert response.status_code == 200, (
        f"Error getting student {student_name} Grades - {response.text}"
    )
    grades = response.json()
    if not grades:
        return 0.0
    return sum(grades.values()) / len(grades)


@pytest.mark.mock
class TestMock:
    def test_mock_object(self, mocker: MockFixture):
        mock_object = mocker.Mock()
        # Configuration Attributes
        mock_object.pie = 3.14
        logger.debug(mock_object.pie)
        mock_object.return_value = "Fake function called"
        logger.debug(mock_object())
        mock_object.add.return_value = 5
        logger.debug(mock_object.add(2, 4))
        logger.debug(mock_object.add(7, 8, 5, 10))
        mock_object.iter.side_effect = ["line1", "line2", "line3"]
        logger.debug(
            f"{mock_object.iter()}, {mock_object.iter()}, {mock_object.iter()}"
        )
        mock_object.iter.side_effect = StopIteration("Generator Error")
        with pytest.raises(StopIteration):
            mock_object.iter()
        user = User("Annie")
        fake_user = mocker.Mock(spec=user)
        logger.debug(fake_user.user_name)

    def test_magick_mock(self, mocker: MockFixture):
        magic_object = mocker.MagicMock()
        magic_object.__len__.return_value = 5
        logger.debug(len(magic_object))
        logger.debug(magic_object["a"])
        magic_object.__getitem__.return_value = "b"
        logger.debug(magic_object["a"])

    def test_calculate_gpaf(self, mocker: MockFixture):
        # Create a mock for the api_client
        api_client = mocker.MagicMock()
        # Setup the mock for the GET request
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "math": 90,
            "science": 80,
            "english": 70,
            "history": 100,
        }
        api_client.get.return_value = mock_response
        # Test calculate_gpa
        student_name = "John Doe"
        calculated_gpa = calculate_gpa(api_client, student_name)
        logger.debug(f"Calculated GPA: {calculated_gpa}")
        expected_gpa = sum([90, 80, 70, 100]) / 4
        assert calculated_gpa == expected_gpa
