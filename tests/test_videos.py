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


def test_get_videos(testapp):
    r = testapp.get("/videos", headers=create_tkn(1))

    assert r.status_code == 200
    assert r.get_json() == []


def test_upload_video(testapp):

    r = testapp.post("/videos",
                     json=FIRST_VIDEO_INFO, headers=create_tkn(1))

    data = r.get_json()

    assert r.status_code == 201
    assert data["video_id"] == 1
    for k in FIRST_VIDEO_INFO.keys():
        assert data[k] == FIRST_VIDEO_INFO[k]


def test_upload_private_video(testapp):
    r = testapp.post("/videos",
                     json=SECOND_VIDEO_INFO, headers=create_tkn(2))

    data = r.get_json()

    assert r.status_code == 201
    assert data["video_id"] == 2
    for k in SECOND_VIDEO_INFO.keys():
        assert data[k] == SECOND_VIDEO_INFO[k]


def test_cant_view_vid_wo_tkn(testapp):
    r = testapp.get('/videos/1')

    assert r.status_code == 400


def test_can_view_video(testapp):
    r = testapp.get('/videos/1', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert data["video_id"] == 1
    for k in FIRST_VIDEO_INFO.keys():
        assert data[k] == FIRST_VIDEO_INFO[k]
    assert data["reaction"] == "none"


def test_canT_view_PRIVATE_video(testapp):
    r = testapp.get('/videos/2', headers=create_tkn(1))

    data = r.get_json()
    assert r.status_code == 401


def test_comment_video(testapp):
    r = testapp.post('/videos/1/comments',
                     json={'text': 'My first comment!'}, headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 201
    assert data["comment_id"] == 1
    assert data["text"] == "My first comment!"
    assert data["uuid"] == 2
    assert data["parent_video"] == 1


def test_view_comment(testapp):
    r = testapp.get('/videos/1/comments', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["comment_id"] == 1
    assert data[0]["text"] == "My first comment!"
    assert data[0]["uuid"] == 2
    assert data[0]["parent_video"] == 1


def test_cant_edt_reaction_before_posting(testapp):
    r = testapp.patch('/videos/1/reactions', headers=create_tkn(2), json={"likes_video": True})
    data = r.get_json()
    assert r.status_code == 400


def test_react_to_video(testapp):
    r = testapp.post('/videos/1/reactions',
                     json={'likes_video': True}, headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 201
    assert data['reaction_id'] == 1
    assert data['uuid'] == 2
    assert data['likes_video'] == True
    assert data['parent_video'] == 1


def test_cant_react_twice(testapp):
    r = testapp.post('/videos/1/reactions',
                     json={'likes_video': False}, headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 400


def test_edit_react_info(testapp):
    r = testapp.patch('/videos/1/reactions', headers=create_tkn(2), json={"likes_video": True})
    data = r.get_json()
    assert r.status_code == 200


def test_view_reactions(testapp):
    r = testapp.get('/videos/1/reactions', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]['reaction_id'] == 1
    assert data[0]['uuid'] == 2
    assert data[0]['likes_video'] == True
    assert data[0]['parent_video'] == 1


def test_count_reactions(testapp):
    r = testapp.get('/videos/1', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 200
    assert data['likes'] == 1
    assert data['dislikes'] == 0


def test_view_vids_by(testapp):
    r = testapp.get('/users/1/videos', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["video_id"] == 1
    for k in FIRST_VIDEO_INFO.keys():
        assert data[0][k] == FIRST_VIDEO_INFO[k]
    assert data[0]["reaction"] == "none"

def test_error_if_unknown_user(testapp):
    r = testapp.get('/users/99999999999/videos', headers=create_tkn(1))
    assert r.status_code == 404

def test_edit_vid_info(testapp):
    r = testapp.patch('/videos/1', headers=create_tkn(1), json={"title": "primer video!"})
    data = r.get_json()
    assert r.status_code == 200
    assert data['title'] == "primer video!"

def test_other_cant_delete_video(testapp):
    r = testapp.delete('/videos/1', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 400

    #vid still exists
    r = testapp.get('/videos/1', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 200
    assert data["video_id"] == 1
    assert data["reaction"] == "like"


def test_pop(testapp):
    r = testapp.get("/videos", headers=create_tkn(2))
    data = r.get_json()

    # vid 2 has no interactions, must have worse popularity

    assert r.status_code == 200
    assert data[0]["popularity"] > data[1]["popularity"]
    assert data[0]["video_id"] == 1


def test_search1(testapp):
    r = testapp.get("/videos?search=primer", headers=create_tkn(2))
    data = r.get_json()

    assert r.status_code == 200
    assert data[0]["video_id"] == 1
    assert len(data) == 1


def test_search2(testapp):
    r = testapp.get("/videos?search=vid", headers=create_tkn(2))
    data = r.get_json()

    assert r.status_code == 200
    assert data[0]["video_id"] == 1
    assert data[1]["video_id"] == 2
    assert len(data) == 2


def test_delete_video(testapp):
    r = testapp.delete('/videos/1', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200

def test_video_doesnt_exist_anymore(testapp):
    r = testapp.get('/videos/1', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 404

def test_reactions_dont_exist_anymore(testapp):
    r = testapp.get('/videos/1/reactions', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 404

def test_no_video_at_user_profile(testapp):
    r = testapp.get('/users/1/videos', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 0
