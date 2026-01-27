import pytest


@pytest.fixture
def data():
    return [1, 2, 3]


def test_one(data):
    data = [1, 2, 3]
    assert 2 in data
    print(data)


def test_two(data):
    print(len(data))
    assert len(data) == 3
