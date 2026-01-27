import pytest
import sys
import os

# Add the parent directory to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.calculator import add, subtract

def test_add_function():
    print("Testing add function")
    assert add(10, 5) == 15

def test_subtract_function():
    print("Testing subtract function")
    assert subtract(10, 5) == 5
