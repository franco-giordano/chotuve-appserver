from datetime import datetime
from app import db

from exceptions.exceptions import NotFoundError


class Chat(db.Model):

    __tablename__ = 'chats'

    user1_id = db.Column(db.Integer, primary_key=True)
    user2_id = db.Column(db.Integer, primary_key=True)

    messages = db.relationship('Message', backref='chat', passive_deletes=True)

    def __repr__(self):
        return '<Chat {}-{}>'.format(self.user1_id, self.user2_id)

    def serialize(self):
        return {
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            "messages": [m.serialize() for m in self.messages]
        }


class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    sender_id =  db.Column(db.Integer, nullable=False)

    recver_id = db.Column(db.Integer, nullable=False)

    text = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    chat_user1 = db.Column(db.Integer, nullable=False)
    chat_user2 = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.ForeignKeyConstraint(['chat_user1', 'chat_user2'],['chats.user1_id', 'chats.user2_id'], ondelete='CASCADE'),)
    

    def __repr__(self):
        return '<Message {}-{}>'.format(self.id, self.timestamp)

    def serialize(self):
        return {
            'id':self.id,
            "sender_id": self.sender_id,
            "recver_id":self.recver_id,
            "text":self.text,
            "timestamp":str(self.timestamp)
        }