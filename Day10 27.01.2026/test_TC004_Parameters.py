import pytest


@pytest.mark.parametrize("a, b, res", [(1, 2, 3), (3, 4, 7)])
def test_add_parameters(a, b, res):
    print(f"Adding {a} and {b} to get {res}")
    assert a + b == res
    

@pytest.mark.smoke
def test_smoke():
    assert True

@pytest.mark.skip(reason="Not ready yet")
def test_skip():
    pass
