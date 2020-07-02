from app import db


import daos.videos_dao

from models.video_elements import VideoReaction

from exceptions.exceptions import BadRequestError

import logging


class ReactionDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def add_rctn(cls, vid_id, uuid, likes):
        new_rctn = VideoReaction(uuid=uuid, likes_video=likes)
        original_vid = daos.videos_dao.VideoDAO.get_raw(vid_id)

        cls.logger().debug(f"Checking if user {uuid} already reacted to vid {vid_id}...")

        for r in original_vid.reactions:
            if r.uuid == uuid:
                raise BadRequestError(
                    f"User {uuid} already reacted to this video.")

        new_rctn.video = original_vid

        db.session.add(new_rctn)
        db.session.commit()

        cls.logger().info(f"New reaction! Added to video {vid_id}. Is a like: {likes}, by {uuid}")
        return new_rctn.serialize()

    @classmethod
    def get_all_from(cls, vid_id):
        vid = daos.videos_dao.VideoDAO.get_raw(vid_id)
        cls.logger().info(f"Serializing all reactions for vid {vid_id}")
        return [r.serialize() for r in vid.reactions]

    @classmethod
    def reaction_by(cls, vid_id, uuid):
        reactions = cls.get_all_from(vid_id)

        reaction = "none"

        cls.logger().debug(f"Checking if user {uuid} reacted to video {vid_id}...")
        for r in reactions:
            if r['uuid'] == uuid:
                reaction = "like" if r['likes_video'] else "dislike"
                cls.logger().info(f"Reaction from user {uuid} found for video {vid_id}. Reaction: {reaction}")

        return reaction

    @classmethod
    def edit_rctn(cls, vid_id, uuid, likes):
        original_vid = daos.videos_dao.VideoDAO.get_raw(vid_id)

        cls.logger().debug(f"Checking if user {uuid} already reacted to vid {vid_id}...")

        for r in original_vid.reactions:
            if r.uuid == uuid:
                r.likes_video = likes
                db.session.commit()
                cls.logger().info(f"Reaction from user {uuid} edited for video {vid_id}. New reaction is a like: {likes}")
                return
        
        raise BadRequestError(f"User {uuid} hasn't reacted to video {vid_id} yet, try POST'ing one first.")