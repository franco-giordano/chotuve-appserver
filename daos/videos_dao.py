from app import db
from models.video_elements import Video

import daos.reactions_dao
from daos.users_dao import FriendshipsDAO
from services.mediasender import MediaSender

import logging

from exceptions.exceptions import NotFoundError, UnauthorizedError

class VideoDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

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

        if vid["is_private"] and not FriendshipsDAO.are_friends(viewer_uuid, vid['uuid']):
            raise UnauthorizedError(f"Trying to access private video, while not being friends with the author")

        cls.add_extra_info(vid, viewer_uuid)

        return vid

    @classmethod
    def get_raw(cls, vid_id):
        vid =  Video.query.get(vid_id)

        if not vid:
            raise NotFoundError(f"No video found with ID: {vid_id}")

        return vid

    @classmethod
    def get_videos_by(cls, user_id, viewer_uuid):
        videos = [v.serialize() for v in Video.query.filter(Video.uuid == user_id)]

        for v in videos:
            cls.add_extra_info(v, viewer_uuid)

        return videos

    @classmethod
    def add_extra_info(cls, serialized_vid, viewer_uuid):
        
        cls.logger().debug(f"Requesting extra info from mediasv, for viewer {viewer_uuid}")
        serialized_vid['firebase_url'], serialized_vid['timestamp'] = MediaSender.get_info(serialized_vid['video_id'])
        serialized_vid['reaction'] = daos.reactions_dao.ReactionDAO.reaction_by(serialized_vid['video_id'], viewer_uuid)

