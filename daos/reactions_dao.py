from app import db


import daos.videos_dao

from models.video_elements import VideoReaction

from exceptions.exceptions import BadRequestError


class ReactionDAO():

    @classmethod
    def add_rctn(cls, vid_id, uuid, likes):
        new_rctn = VideoReaction(uuid=uuid, likes_video=likes)
        original_vid = daos.videos_dao.VideoDAO.get_raw(vid_id)

        for r in original_vid.reactions:
            if r.uuid == uuid:
                raise BadRequestError(
                    f"User {uuid} already reacted to this video.")

        new_rctn.video = original_vid

        db.session.add(new_rctn)
        db.session.commit()

        return new_rctn.serialize()

    @classmethod
    def get_all_from(cls, vid_id):
        vid = daos.videos_dao.VideoDAO.get_raw(vid_id)

        return [r.serialize() for r in vid.reactions]

    @classmethod
    def reaction_by(cls, vid_id, uuid):
        reactions = cls.get_all_from(vid_id)

        reaction = "none"

        for r in reactions:
            if r['uuid'] == uuid:
                reaction = "like" if r['likes_video'] else "dislike"

        return reaction
