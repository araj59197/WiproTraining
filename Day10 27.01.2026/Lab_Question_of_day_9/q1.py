# Sample function (logic would normally go in utilities/)
def add(a, b):
    return a + b

# Sample Test Case (tests would normally go in tests/)
import pytest

def test_sample_add():
    result = add(10, 5)
    assert result == 15
    print('Sample test passed!')
