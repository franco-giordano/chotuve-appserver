from app import db
from datetime import datetime


class HTTPResponse(db.Model):

    __tablename__ = "http_responses"

    id = db.Column(db.Integer, primary_key=True)

    path = db.Column(db.String(200))
    method = db.Column(db.String(100))
    response_code = db.Column(db.Integer)
    client_ip = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<HTTPResponse {}>'.format(self.id)

