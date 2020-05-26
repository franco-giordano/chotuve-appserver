import pytest

def sum(x, y):
    return x + y

def test_answer():
    assert sum(3, 4) == 7

def test_answer2():
    assert sum(2, 2) == 4