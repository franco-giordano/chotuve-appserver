from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# modelo
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    author_user = db.Column(db.Integer)

    def __init__(self, title, description, author_user):
        self.title = title
        self.description = description
        self.author_user = author_user

# vid shema ?????

class VideoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'author_user')


# sino se queja la terminal
video_schema = VideoSchema()

videos_schema = VideoSchema(many=True)


videos = [
    {
        'author_user': 'Frank',
        'title': 'Mi Tutorial',
        'desc': 'Mi primer tutorial!',
    },
    {
        'author_user': 'Frank',
        'title': 'Mis vacaciones',
        'desc': 'Mi primer vlog',
    }
]


@app.route('/video', methods=['POST'])
def add_video():

    if not request.json or not 'author_user' in request.json or not 'title' in request.json:
        abort(400)
    
    author_user = request.json['author_user']
    title = request.json['title']
    description = request.json['description']

    new_vid = Video(title, description,author_user)

    db.session.add(new_vid)
    db.session.commit()

    return video_schema.jsonify(new_vid)

@app.route('/video', methods=['GET'])
def get_videos():
    all_vids = Video.query.all()
    result = videos_schema.dump(all_vids)

    return jsonify(result)

@app.route('/video/<id>', methods=['GET'])
def get_single_vid(id):
    vid = Video.query.get(id)

    if not vid:
        abort(404)

    return video_schema.jsonify(vid)


@app.route('/video/<id>', methods=['PUT'])
def edit_video(id):
    original_vid = Video.query.get(id)

    author_user = request.json['author_user']
    title = request.json['title']
    description = request.json['description']

    original_vid.author_user = author_user
    original_vid.title = title
    original_vid.description = description

    db.session.commit()

    return video_schema.jsonify(original_vid)


@app.route('/video/<id>', methods=['DELETE'])
def delete_single_vid(id):
    vid = Video.query.get(id)

    db.session.delete(vid)
    db.session.commit()

    return video_schema.jsonify(vid)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 404)




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)