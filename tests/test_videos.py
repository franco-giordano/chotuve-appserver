import pytest

FIRST_VIDEO_INFO = {
            "title":"My first video",
            "description":"my awesome desc",
            "location":"Magic Land",
            "firebase_url":"carlos.com/videos/1"}

SECOND_VIDEO_INFO = {
            "title":"videazo",
            "description":"descripcion",
            "location":"Cosmic Land",
            "firebase_url":"marcos.com/mi_video",
            "is_private":True}

def create_tkn(id):
    return {'x-access-token':str(id)}

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
    r = testapp.post('/videos/1/comments', json={'text':'My first comment!'}, headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 201
    assert data["comment_id"] == 1
    assert data["text"] == "My first comment!"
    assert data["uuid"] == 1
    assert data["parent_video"] == 1


def test_view_comment(testapp):
    r = testapp.get('/videos/1/comments', headers=create_tkn(1))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["comment_id"] == 1
    assert data[0]["text"] == "My first comment!"
    assert data[0]["uuid"] == 1
    assert data[0]["parent_video"] == 1


def test_react_to_video(testapp):
    r = testapp.post('/videos/1/reactions', json={'likes_video':True}, headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 201
    assert data['reaction_id'] == 1
    assert data['uuid'] == 2
    assert data['likes_video'] == True
    assert data['parent_video'] == 1


def test_view_reactions(testapp):
    r = testapp.get('/videos/1/reactions', headers=create_tkn(2))
    data = r.get_json()
    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]['reaction_id'] == 1
    assert data[0]['uuid'] == 2
    assert data[0]['likes_video'] == True
    assert data[0]['parent_video'] == 1