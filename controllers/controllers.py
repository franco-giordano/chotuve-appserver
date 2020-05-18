from models.models import Video, Comment, VideoReaction

from flask import request, jsonify, make_response, abort
from run import app

from app import db

from services.authsender import AuthSender
from services.mediasender import MediaSender

from functools import wraps
import requests, os

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'error' : 'Missing user token!'}, 401)

        if not AuthSender.is_valid_token(token):
            return make_response({'message' : 'Token is invalid!'}, 401)

        return f(*args, **kwargs)

    return decorated

@app.route('/video', methods=['POST'])
@token_required
def add_video():

    if not request.json or not 'username' in request.json:
        abort(400)

    user = request.json['username']
    title = request.json['title']
    description = request.json['description']
    location = request.json['location']
    fb_url = request.json['firebase-url']


    new_vid = Video(title=title, description=description, username=user, location=location)

    MediaSender.send_url_to_mediasv(new_vid.id,fb_url)

    db.session.add(new_vid)
    db.session.commit()

    return jsonify(new_vid.serialize())

    


@app.route('/video', methods=['GET'])
@token_required
def get_videos():
    videos = Video.query.all()
    videos = [v.serialize() for v in videos]

    for video in videos:
        video['firebase-url'] = MediaSender.get_url_from_mediasv(video['video_id'])

    return jsonify(videos)


@app.route('/video/<id>', methods=['GET'])
@token_required
def get_video(id):
    video=Video.query.get(id)

    if not video:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)

    serialized_video = video.serialize()

    serialized_video['firebase-url'] = MediaSender.get_url_from_mediasv(video.id)

    return jsonify(serialized_video)


# @app.route('/video/<id>', methods=['GET'])
# def get_single_vid(id):
#     vid = Video.query.get(id)

#     if not vid:
#         abort(404)

#     return video_schema.jsonify(vid)


@app.route('/video/<id>/comments', methods=['POST'])
@token_required
def post_comment(id):

    if not request.json or not 'comment_username' in request.json:
        abort(400)


    original_vid = Video.query.get(id)

    if not original_vid:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)

    comment_username = request.json['comment_username']
    text = request.json['text']

    new_cmnt = Comment(comment_username=comment_username, text = text)
    new_cmnt.video= original_vid

    db.session.add(new_cmnt)
    db.session.commit()

    return jsonify(new_cmnt.serialize())

@app.route('/video/<id>/comments', methods=['GET'])
@token_required
def get_comments(id):
    original_vid = Video.query.get(id)


    if not original_vid:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)


    return jsonify([c.serialize() for c in original_vid.comments])


@app.route('/video/<id>/reactions', methods=['GET'])
@token_required
def get_reactions(id):
    original_vid = Video.query.get(id)

    if not original_vid:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)

    return jsonify([c.serialize() for c in original_vid.reactions])



@app.route('/video/<id>/reactions', methods=['POST'])
@token_required
def post_reaction(id):

    if not request.json or not 'username' in request.json or not 'likes_video' in request.json:
        abort(400)

    original_vid = Video.query.get(id)

    if not original_vid:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)

    username = request.json['username']
    likes_video = request.json['likes_video']

    for r in original_vid.reactions:
        if r.username == username:
            r.likes_video = likes_video
            db.session.commit()
            return jsonify(r.serialize())

    rctn = VideoReaction(username=username, likes_video=likes_video)
    rctn.video = original_vid

    db.session.add(rctn)
    db.session.commit()

    return jsonify(rctn.serialize())

# @app.route('/video/<id>', methods=['DELETE'])
# def delete_single_vid(id):
#     vid = Video.query.get(id)

#     db.session.delete(vid)
#     db.session.commit()

#     return video_schema.jsonify(vid)

@app.route('/user/<username>/videos', methods=['GET'])
@token_required
def get_videos_by_user(username):
    videos=Video.query.filter(Video.username == username)
    return jsonify([v.serialize() for v in videos])

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'appserver':'UP'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@app.errorhandler(400)
def bad_req(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

# @app.route('/')
# def hi():
#     return "HOLA"