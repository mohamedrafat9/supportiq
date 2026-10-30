import pytest
def add(a, b):
    return a + b

@pytest.mark.parametrize(
       "a, b, expected",
    [
        (10, 20, 30),
        (-10, -20, -30),
        (10, 0, 10),
        (5, -5, 4),
    ],
)
def test_add(a,b,expected):
    assert add(a,b)==expected