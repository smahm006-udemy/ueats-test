import pytest


test_case_data = {"C1234": ["param1", "param2"], "C5678": ["param3", "param4"]}


def apply_discount(value, discount):
    return value * (1 - discount)


@pytest.fixture(params=["viewer", "editor", "admin"])
def role(request):
    role_access = {"viewer": "read", "editor": "read, write", "admin": "all"}
    return request.param, role_access[request.param]


@pytest.mark.parameterization
class TestParameterization:
    # Here’s our test function for calculating discounts
    @pytest.mark.parametrize(
        "price, discount, expected_price",
        [(100, 0.1, 90), (200, 0.2, 160)],
        ids=["one-hundo", "two-hundo"],
    )
    def test_apply_discount(self, price, discount, expected_price):
        new_price = apply_discount(price, discount)
        assert new_price == expected_price, (
            f"Found {discount}% of {price} to be {expected_price} but got {new_price}"
        )

    @pytest.mark.parametrize("uid", [1, 2, 3])
    @pytest.mark.parametrize("gid", [4, 5, 6])
    def test_user_role(self, role, uid, gid):
        role_name, role_permissions = role
        match role_name:
            case "viewer":
                assert role_permissions == "read"
            case "editor":
                assert role_permissions == "read, write"

    @pytest.mark.parametrize("case_id", test_case_data.keys())
    def test_case_ids(self, case_id):
        print(f"Running case id: {case_id} with data {test_case_data[case_id]}")
