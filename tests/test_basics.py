"""
tests/test_basics.py


Basic pytest structure
"""


def test_basic():
    """Test a basic test"""
    print("Hello World")


def test_true_assert():
    """Test a true assert"""
    assert True


def test_false_assert():
    """Test a false assert"""
    try:
        assert False
    except AssertionError:
        assert True
