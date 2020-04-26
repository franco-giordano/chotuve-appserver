from datetime import datetime
from app import db

# modelo
class Video(db.Model):

    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    username = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))

    is_private = db.Column(db.Boolean, default=False)
    likes=db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='video')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Video id {} - {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'video_id': self.id, 
            'title': self.title,
            'description': self.description,
            'username':self.username,
            'location':self.location,
            'is_private': self.is_private,
            'likes':self.likes,
            'dislikes':self.dislikes,
            'timestamp':self.timestamp,
        }

class Comment(db.Model):

    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)

    comment_username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_video = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)

    def __repr__(self):
        return '<Comment {}-{}>'.format(self.author_id, self.timestamp)

    def serialize(self):
        print(self.video)
        return {
            'comment_id': self.id, 
            'comment_username': self.comment_username,
            'text': self.text,
            'timestamp':self.timestamp,
            'parent_video':self.parent_video
        }