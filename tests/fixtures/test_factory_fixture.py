import pytest
from .test_fixtures import logger


class User:
    def __init__(self, username: str, role: str = "user"):
        self.username = username
        self.role = role

    def is_admin(self) -> bool:
        return self.role == "admin"

    def change_role(self, another_user: "User", role: str):
        if not self.is_admin():
            raise PermissionError(
                f"{self.username} is not an admin and cannot change roles."
            )
        another_user.role = role


@pytest.fixture
def user_factory():
    def create_user(username: str, role: str = "user"):
        logger.info(f"Creating user {username} with role {role}")
        return User(username=username, role=role)

    return create_user


@pytest.mark.fixture
class TestFactoryFixture:
    def test_user_factory(self, user_factory):
        admin_user: User = user_factory("Mark", "admin")
        assert admin_user.is_admin()
        editor_user: User = user_factory("Annie", "editor")
        assert not editor_user.is_admin()

    @pytest.mark.parametrize(
        "username, role, is_admin",
        [
            ("viewer_user", "viewer", False),
            ("editor_user", "editor", False),
            ("admin_user", "admin", True),
        ],
    )
    def test_user_parameterized(self, user_factory, username, role, is_admin):
        dummy_user: User = user_factory("John", "viewer")
        parameterized_user: User = user_factory(username, role)

        if parameterized_user.role == "admin":
            parameterized_user.change_role(dummy_user, "editor")
            assert dummy_user.role == "editor"
        else:
            with pytest.raises(PermissionError):
                parameterized_user.change_role(dummy_user, "editor")
