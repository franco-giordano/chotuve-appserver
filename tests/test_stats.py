import pytest

def test_stats(testapp):
    r = testapp.get('/stats')

    print(r.get_json())