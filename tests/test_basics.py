"""
tests/test_basics.py


Basic pytest structure
"""


def test_basic():
    """Test a basic test"""
    print("Hello World")


def test_one_plus_one():
    """Test to verify one plus one is two"""
    if 1 + 1 != 2:
        raise ValueError("one plus one did not equal two")


def test_assert():
    """Test a truthful assert"""
    assert 1 + 1 == 2, "one plus one did not equal two"
