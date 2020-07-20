from app import db

from daos.videos_dao import VideoDAO

from models.video_elements import Comment

from services.notifications_creator import NotificationsCreator
from services.authsender import AuthSender

import logging

class CommentDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def add_cmnt(cls, vid_id, uuid, text, time, tkn):
        new_cmnt = Comment(uuid=uuid, text=text, vid_time=time)
        vid = VideoDAO.get_raw(vid_id)
        new_cmnt.video = vid

        db.session.add(new_cmnt)
        db.session.commit()
        cls.logger().info(f"Succesfully appended comment to video {vid_id}. Comment: {new_cmnt.serialize()}")


        # Notification build w/tkn...
        cmnt_author = AuthSender.get_author_name(uuid, tkn)

        if uuid != vid.uuid:
            NotificationsCreator.notify_new_comment(vid.uuid, vid_id, vid.title, text, cmnt_author)

        return new_cmnt.serialize()

    @classmethod
    def get_all_from(cls, vid_id):
        vid = VideoDAO.get_raw(vid_id)

        count = vid.increase_view_count()
        cls.logger().info(f"Increased view count for vid {vid_id}. New count: {count}")

        cls.logger().info(f"Serializing comments for vid {vid_id}...")
        return [c.serialize() for c in vid.comments]
