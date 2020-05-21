from app import db
from run import app
from models.models import Video
from flask_restful import abort

class VideoDAO():

    @classmethod
    def add_vid(cls, title, description, uuid, location, is_private):
        
        new_vid = Video(title=title, description=description, uuid=uuid, 
                        location=location, is_private=is_private)
        db.session.add(new_vid)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return [v.serialize() for v in Video.query.all()]

    @classmethod
    def get(cls, vid_id):
        vid = cls.get_raw(vid_id)

        return vid.serialize()

    @classmethod
    def get_raw(cls, vid_id):
        vid =  Video.query.get(vid_id)

        if not vid:
            abort(404, message="No video found with this ID")

        return vid

