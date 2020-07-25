import pytest
from tests.tools import *


FIRST_VIDEO_INFO = {
    "title": "My first video",
    "description": "my awesome desc",
    "location": "Magic Land",
    "firebase_url": "carlos.com/videos/1",
    "thumbnail_url":"www.google.com/thumbnail1"}


SECOND_VIDEO_INFO = {
    "title": "videazo",
    "description": "descripcion",
    "location": "Cosmic Land",
    "firebase_url": "marcos.com/mi_video",
    "is_private": True,
    "thumbnail_url":"www.google.com/thumbnail2"}

def test_cant_delete_others_accounts(testapp):
    r = testapp.delete("/users/1", headers=create_tkn(2))
    assert r.status_code == 400



def test_delete_user(testapp):
    # upload a vid
    r = testapp.post("/videos",
                     json=FIRST_VIDEO_INFO, headers=create_tkn(1))

    # react to vid
    r = testapp.post('/videos/2/reactions', json={'likes_video': True}, headers=create_tkn(1))

    # comment vid
    r = testapp.post('/videos/2/comments', json={'text': "epico"}, headers=create_tkn(1))

    # add friend
    r = testapp.post('/friend-requests', headers=create_tkn(2), json={"to":1})
    r = testapp.post('/friend-requests/2',
                     json={'accept': True}, headers=create_tkn(1))


    r = testapp.delete("/users/1", headers=create_tkn(1))
    assert r.status_code == 200

    r = testapp.get("/users/1/videos", headers=create_tkn(2))
    assert r.status_code == 404

    r = testapp.get("/messages/2?page=1&per_page=20", headers=create_tkn(1))
    assert r.status_code == 404

    r = testapp.get("/users/2/friends", headers=create_tkn(2))
    assert r.get_json()["friends"] == []

    r = testapp.get("/videos", headers=create_tkn(2))
    assert len(r.get_json()["videos"]) == 1

    data = testapp.get("/videos/2/reactions", headers=create_tkn(2)).get_json()
    assert data == []

    data = testapp.get("/videos/2/comments", headers=create_tkn(2)).get_json()
    assert data == []


