from datetime import datetime
from app import db

# modelo


class Video(db.Model):

    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    uuid = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200))
    thumbnail_url = db.Column(db.String(100))


    is_private = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='video')
    reactions = db.relationship(
        'VideoReaction', backref='video', lazy="subquery")

    # EL TIMESTAMP LO GUARDA EL MEDIASV!!!

    def count_likes(self):
        likes = 0
        for r in self.reactions:
            likes += int(r.likes_video)
        return likes

    def count_dislikes(self):
        dislikes = 0
        for r in self.reactions:
            dislikes += int(not r.likes_video)
        return dislikes

    def __repr__(self):
        return '<Video id {} - {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'video_id': self.id,
            'title': self.title,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'uuid': self.uuid,
            'location': self.location,
            'is_private': self.is_private,
            'likes': self.count_likes(),
            'dislikes': self.count_dislikes(),
        }


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    vid_time = db.Column(db.String(10))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_video = db.Column(
        db.Integer, db.ForeignKey('videos.id'), nullable=False)

    def __repr__(self):
        return '<Comment {}-{}>'.format(self.uuid, self.timestamp)

    def serialize(self):
        return {
            'comment_id': self.id,
            'uuid': self.uuid,
            'text': self.text,
            'timestamp': str(self.timestamp),
            'parent_video': self.parent_video,
            'vid_time': self.vid_time
        }


class VideoReaction(db.Model):

    __tablename__ = 'video_reactions'

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.Integer, nullable=False)
    likes_video = db.Column(db.Boolean, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_video = db.Column(
        db.Integer, db.ForeignKey('videos.id'), nullable=False)

    def __repr__(self):
        return '<Reaction {}-{}>'.format(self.uuid, self.likes_video)

    def serialize(self):
        return {
            'reaction_id': self.id,
            'uuid': self.uuid,
            'likes_video': self.likes_video,
            'timestamp': str(self.timestamp),
            'parent_video': self.parent_video
        }
