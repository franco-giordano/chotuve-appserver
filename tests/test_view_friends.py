import pytest
from tests.tools import *


def test_no_friends(testapp):
    a = testapp.get('/users/1/friends', headers=create_tkn(1))
    b = testapp.get('/users/2/friends', headers=create_tkn(1))

    assert a.status_code == 200
    assert a.get_json()["friends"] == []

    assert b.status_code == 200
    assert b.get_json()["friends"] == []


def test_send_request(testapp):
    r = testapp.post('/users/1/friends/requests', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 201
    assert data["sent_reqs"][0]["user_id"] == 1
    assert len(data["sent_reqs"]) == 1


def test_cant_spam_multiple_reqs(testapp):
    r = testapp.post('/users/1/friends/requests', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 400


def test_can_view_reqs(testapp):
    r = testapp.get('/users/1/friends/requests', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert data["pending_reqs"][0]["user_id"] == 2
    assert len(data["pending_reqs"]) == 1


def test_cant_view_others_reqs(testapp):
    r = testapp.get('/users/1/friends/requests', headers=create_tkn(2))

    assert r.status_code == 401


def test_cant_send_req_to_pending_user(testapp):
    r = testapp.post('/users/2/friends/requests', headers=create_tkn(1))
    assert r.status_code == 400


def test_cant_accept_other_user_req(testapp):
    r = testapp.post('/users/2/friends/requests/1',
                     json={'accept': True}, headers=create_tkn(2))

    # no req found
    assert r.status_code == 404

    # didnt affect original req
    r = testapp.get('/users/1/friends/requests', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert data["pending_reqs"][0]["user_id"] == 2
    assert len(data["pending_reqs"]) == 1


def test_cant_accept_other_user_req_v2(testapp):
    r = testapp.post('/users/1/friends/requests/2',
                     json={'accept': True}, headers=create_tkn(2))

    assert r.status_code == 401


def test_must_send_jsonresponse(testapp):
    r = testapp.post('/users/1/friends/requests/2', headers=create_tkn(1))

    assert r.status_code == 400


def test_can_reject_req(testapp):
    r = testapp.post('/users/1/friends/requests/2',
                     json={'accept': False}, headers=create_tkn(1))

    assert r.status_code == 200

    # deletes req
    r = testapp.get('/users/1/friends/requests', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert data["pending_reqs"] == []


def test_can_accept_req(testapp):
    r = testapp.post('/users/1/friends/requests', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 201
    assert data["sent_reqs"][0]["user_id"] == 1
    assert len(data["sent_reqs"]) == 1

    r = testapp.post('/users/1/friends/requests/2',
                     json={'accept': True}, headers=create_tkn(1))
    assert r.status_code == 200


def test_now_friends(testapp):
    r = testapp.get('/users/1/friends', headers=create_tkn(1))
    data = r.get_json()

    assert data["friends"][0]["user_id"] == 2
    assert len(data["friends"]) == 1

    r = testapp.get('/users/2/friends', headers=create_tkn(1))
    data = r.get_json()

    assert data["friends"][0]["user_id"] == 1
    assert len(data["friends"]) == 1


def test_cant_add_myself(testapp):
    r = testapp.post('/users/1/friends/requests', headers=create_tkn(1))

    assert r.status_code == 400
