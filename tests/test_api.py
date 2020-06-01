import pytest
from tests.conftest import *

def test_ping(testapp):
    response = testapp.get('/ping')

    json_data = response.get_json()
    assert json_data['appserver'] == 'UP'
    assert response.status_code == 200