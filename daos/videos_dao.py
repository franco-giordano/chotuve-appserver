from app import db
from run import app
from models.models import Video
from flask_restful import abort

import daos.reactions_dao
from services.mediasender import MediaSender

class VideoDAO():

    @classmethod
    def add_vid(cls, title, description, uuid, location, is_private):
        
        new_vid = Video(title=title, description=description, uuid=uuid, 
                        location=location, is_private=is_private)
        db.session.add(new_vid)
        db.session.commit()

        return new_vid.serialize()

    @classmethod
    def get_all(cls, viewer_uuid):
        all_vids = Video.query.all()
        
        final_vids = []

        for v in all_vids:
            res = v.serialize()
            cls.add_extra_info(res, viewer_uuid)
            final_vids.append(res)

        return final_vids


    @classmethod
    def get(cls, vid_id, viewer_uuid):
        vid = cls.get_raw(vid_id).serialize()

        cls.add_extra_info(vid, viewer_uuid)

        return vid

    @classmethod
    def get_raw(cls, vid_id):
        vid =  Video.query.get(vid_id)

        if not vid:
            abort(404, message="No video found with this ID")

        return vid

    @classmethod
    def get_videos_by(cls, user_id, viewer_uuid):
        videos = [v.serialize() for v in Video.query.filter(Video.uuid == user_id)]

        for v in videos:
            cls.add_extra_info(v, viewer_uuid)

        return videos

    @classmethod
    def add_extra_info(cls, serialized_vid, viewer_uuid):
        
        serialized_vid['firebase-url'], serialized_vid['timestamp'] = MediaSender.get_info(serialized_vid['video_id'])
        serialized_vid['reaction'] = daos.reactions_dao.ReactionDAO.reaction_by(serialized_vid['video_id'], viewer_uuid)

