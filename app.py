from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Video, Comment




@app.route('/video', methods=['POST'])
def add_video():

    if not request.json or not 'username' in request.json:
        abort(400)

    user = request.json['username']
    title = request.json['title']
    description = request.json['description']
    location = request.json['location']

    new_vid = Video(title=title, description=description, username=user, location=location)

    db.session.add(new_vid)
    db.session.commit()

    return jsonify(new_vid.serialize())

    


@app.route('/video', methods=['GET'])
def get_videos():
    videos=Video.query.all()
    return jsonify([v.serialize() for v in videos])


# @app.route('/video/<id>', methods=['GET'])
# def get_single_vid(id):
#     vid = Video.query.get(id)

#     if not vid:
#         abort(404)

#     return video_schema.jsonify(vid)


@app.route('/video/<id>/comments', methods=['POST'])
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
def get_comments(id):
    original_vid = Video.query.get(id)


    if not original_vid:
        return make_response(jsonify({'error': 'No video found with this ID'}), 404)


    return jsonify([c.serialize() for c in original_vid.comments])

# @app.route('/video/<id>', methods=['DELETE'])
# def delete_single_vid(id):
#     vid = Video.query.get(id)

#     db.session.delete(vid)
#     db.session.commit()

#     return video_schema.jsonify(vid)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


# @app.errorhandler(400)
# def not_found(error):
#     return make_response(jsonify({'error': 'Bad Request'}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)