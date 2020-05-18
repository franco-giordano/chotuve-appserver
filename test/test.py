from run import app
import pytest

def sum(x,y):
    return x+y

def test_answer():
    assert sum(3,4) == 7