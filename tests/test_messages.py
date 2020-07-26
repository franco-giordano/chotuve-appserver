import pytest
from tests.tools import *

MESSAGE = {"text":"HOLA!"}

def test_cant_send_to_non_friend(testapp):
    r = testapp.post('/messages/1', headers=create_tkn(2), json=MESSAGE)
    assert r.status_code == 400

def test_cant_send_to_myself(testapp):
    r = testapp.post('/messages/1', headers=create_tkn(1), json=MESSAGE)
    assert r.status_code == 400


def test_not_null_message(testapp):
    r = testapp.post('/friend-requests', headers=create_tkn(2), json={"to":1})
    r = testapp.post('/friend-requests/2',
                     json={'accept': True}, headers=create_tkn(1))
    
    r = testapp.get('/users/1/friends', headers=create_tkn(1))
    data = r.get_json()

    assert data["friends"][0]["user_id"] == 2
    assert len(data["friends"]) == 1

    # send a message
    r = testapp.post('/messages/1', headers=create_tkn(2), json={"text":""})
    assert r.status_code == 400

def test_no_msgs(testapp):
    r = testapp.get('/messages/2?page=1&per_page=20', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 0


def test_error_if_unknown_recipient(testapp):
    r = testapp.get('/messages/999999999999?page=1&per_page=20', headers=create_tkn(1))
    assert r.status_code == 404

def test_send_message(testapp):

    # send a message
    r = testapp.post('/messages/1', headers=create_tkn(2), json=MESSAGE)
    assert r.status_code == 201

def test_read_msg(testapp):
    r = testapp.get('/messages/2?page=1&per_page=20', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert data[0]["sender_id"] == 2
    assert data[0]["recver_id"] == 1
    assert data[0]["text"] == "HOLA!"
    assert len(data) == 1

def test_cant_send_after_deleting_friendship(testapp):
    r = testapp.delete('/users/2/friends/1', headers=create_tkn(2))

    r = testapp.post('/messages/1', headers=create_tkn(2))

    assert r.status_code == 400