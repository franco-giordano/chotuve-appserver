from app import db

from models.friends_elements import User

import logging

# from exceptions.exceptions import VideoNotFoundError

class FriendshipsDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def add_friendship(cls, user1_id, user2_id):
        
        new_user = User(id=user_id)
        db.session.add(new_user)
        db.session.commit()

        return new_user.serialize()

    @classmethod
    def get_friends(cls, user_id):
        user =  User.query.get(user_id)

        return user.serialize()['friends']