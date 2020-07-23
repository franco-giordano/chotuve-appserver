from app import db
from models.video_elements import Video

import daos.reactions_dao
from daos.users_dao import UsersDAO
from services.mediasender import MediaSender
from services.authsender import AuthSender

from dateutil.parser import parse
import datetime

import logging

from exceptions.exceptions import NotFoundError, UnauthorizedError, BadRequestError


class VideoDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def add_vid(cls, title, description, uuid, location, is_private, thumbnail_url):

        new_vid = Video(title=title, description=description, uuid=uuid,
                        location=location, is_private=is_private, thumbnail_url=thumbnail_url)
        db.session.add(new_vid)
        db.session.commit()

        cls.logger().info(f"New video uploaded: {new_vid.serialize()}")

        return new_vid.serialize()

    @classmethod
    def get_all(cls, viewer_uuid, token):
        all_vids = Video.query.all()

        final_vids = []

        for v in all_vids:
            res = v.serialize()

            if cls._cant_view(res["is_private"], res["uuid"], viewer_uuid):
                continue

            cls.add_extra_info(res, viewer_uuid)
            res["author"] = AuthSender.get_author_name(res["uuid"], token)
            final_vids.append(res)

        return final_vids


    @classmethod
    def get_from_search(cls, viewer_uuid, token, title_query):
        all_vids = Video.query.filter(Video.title.contains(title_query)).limit(20).all()

        return cls._add_info_and_popularity(all_vids, viewer_uuid, token)


    @classmethod
    def get_recommendations(cls, viewer_uuid, token):
        all_vids = Video.query.order_by(Video.cached_relevance.desc()).limit(50).all()

        return cls._add_info_and_popularity(all_vids, viewer_uuid, token, sort_by_pop=True)



    @classmethod
    def _add_info_and_popularity(cls, all_vids, viewer_uuid, token, sort_by_pop=False):

        final_vids = []

        for v in all_vids:
            res = v.serialize()

            if cls._cant_view(res["is_private"], res["uuid"], viewer_uuid):
                continue

            cls.add_extra_info(res, viewer_uuid)
            res["author"] = AuthSender.get_author_name(res["uuid"], token)
            if sort_by_pop:
                res["popularity"] = cls._calculate_popularity(v, viewer_uuid, res["timestamp"])
            final_vids.append(res)

        if sort_by_pop:
            final_vids = sorted(final_vids, key=lambda k: k['popularity'], reverse=True)

        return final_vids

    @classmethod
    def _calculate_popularity(cls, video, viewer_uuid, timestamp):

        friendship_bonus = int(UsersDAO.are_friends(video.uuid, viewer_uuid))*10

        influencer_bonus = UsersDAO.count_friends(video.uuid)*2

        time_bonus =  60 / (cls._minutes_passed(timestamp)/1440 + 1)

        return video.cached_relevance + friendship_bonus + int(time_bonus) + influencer_bonus


    @classmethod
    def _minutes_passed(cls, old_timestamp):
        date = datetime.datetime.now(datetime.timezone.utc) - parse(old_timestamp)
        return int(date.days*24*60 + date.seconds/60)

    @classmethod
    def get(cls, vid_id, viewer_uuid):
        vid = cls.get_raw(vid_id).serialize()

        if cls._cant_view(vid["is_private"], viewer_uuid, vid['uuid']):
            raise UnauthorizedError(
                f"Trying to access private video, while not being friends with the author")

        cls.add_extra_info(vid, viewer_uuid)

        return vid

    @classmethod
    def edit(cls, vid_id, args, uuid):
        vid = cls.get_raw(vid_id)

        if not AuthSender.has_permission(vid.uuid, uuid):
            raise BadRequestError(f"Only the author can edit their video!")

        if args["description"]:
            vid.description = args["description"]
        if args["location"]:
            vid.location = args["location"]
        if args["title"]:
            vid.title = args["title"]
        if args["is_private"]:
            vid.is_private = args["is_private"]

        db.session.commit()

        return vid.serialize()

    @classmethod
    def delete(cls, vid_id, actioner_uuid):
        vid = cls.get_raw(vid_id)

        if not AuthSender.has_permission(vid.uuid, actioner_uuid):
            raise BadRequestError("Only the author can delete their video!")

        vid.comments = []
        vid.reactions = []

        db.session.delete(vid)
        db.session.commit()


    @classmethod
    def get_raw(cls, vid_id):
        vid = Video.query.get(vid_id)

        if not vid:
            raise NotFoundError(f"No video found with ID: {vid_id}")

        return vid

    @classmethod
    def get_videos_by(cls, user_id, viewer_uuid, token):
        cls.logger().info(f"Grabbing all videos by user {user_id}")
        videos = [v.serialize()
                  for v in Video.query.filter(Video.uuid == user_id)]

        cls.logger().info(f"Filtering by viewable videos for viewer {viewer_uuid}")
        filtered = [f for f in videos if not cls._cant_view(f["is_private"], viewer_uuid, user_id)]

        for f in filtered:
            cls.add_extra_info(f, viewer_uuid)
            f["author"] = AuthSender.get_author_name(f["uuid"], token)

        cls.logger().info(f"Found {len(filtered)} viewable videos uploaded by user {user_id}")
        return filtered

    @classmethod
    def add_extra_info(cls, serialized_vid, viewer_uuid):

        cls.logger().debug(
            f"Requesting extra info from mediasv, for viewer {viewer_uuid}")
        serialized_vid['firebase_url'], serialized_vid['timestamp'] = MediaSender.get_info(
            serialized_vid['video_id'])
        serialized_vid['reaction'] = daos.reactions_dao.ReactionDAO.reaction_by(
            serialized_vid['video_id'], viewer_uuid)
    


    @classmethod
    def _cant_view(cls, is_private, user1_id, user2_id):
        return is_private and not AuthSender.has_permission(user1_id, user2_id) and not UsersDAO.are_friends(user1_id, user2_id)