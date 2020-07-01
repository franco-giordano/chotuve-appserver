from app import db

from models.users_elements import User

import logging

from exceptions.exceptions import NotFoundError, BadRequestError, InternalError

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError



class UsersDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def add_friendship(cls, rcv_id, sender_id):

        snd = cls.get_raw(sender_id)
        rcv = cls.get_raw(rcv_id)

        snd.friends.append(rcv)
        rcv.friends.append(snd)
        db.session.commit()

        cls.logger().debug(snd.serializeFriends())
        cls.logger().debug(rcv.serializeFriends())

        return rcv.serializeFriends()

    @classmethod
    def get_friends(cls, user_id):
        user = cls.get_raw(user_id)

        return user.serializeFriends()

    @classmethod
    def get_raw(cls, user_id):
        user = User.query.get(user_id)

        if not user:
            raise NotFoundError(f"No user found with ID {user_id}")

        return user

    @classmethod
    def create_raw(cls, user_id):
        try:
            new_user = User(id=user_id)
            db.session.add(new_user)
            db.session.commit()
        except (UniqueViolation, IntegrityError) as e:
            cls.logger().error(e)
            raise InternalError(f"User already exists with ID {user_id}")

        return new_user

    @classmethod
    def add_user_to_db(cls, user_id):
        cls.create_raw(user_id)

    @classmethod
    def send_request(cls, snd_id, rcv_id):
        if snd_id == rcv_id:
            raise BadRequestError(
                "You can't send a friend request to yourself!")

        snd = cls.get_raw(snd_id)
        rcv = cls.get_raw(rcv_id)

        if rcv.received_request_from(snd) or snd.is_friend_with(rcv):
            raise BadRequestError(
                f"You already sent a request, or are already friends.")

        if snd.received_request_from(rcv):
            raise BadRequestError(
                f"You have a pending request from this user, try accepting or rejecting it first.")

        snd.sent_requests.append(rcv)
        db.session.commit()

        cls.logger().debug(f"Sent requests: {snd.serializeSentReqs()}")
        cls.logger().debug(f"Received reqs: {rcv.serializeReceivedReqs()}")
        

        from services.usernotifier import UserNotifier, MessageTypes
        UserNotifier.send_notification(rcv_id, "Nueva solicitud de amistad", "Ve a la seccion notificaciones!", MessageTypes.FRIEND_REQ.value, {})


        return snd.serializeSentReqs(), 201

    @classmethod
    def view_pending_reqs(cls, user_id):
        user = cls.get_raw(user_id)

        return user.serializeReceivedReqs()

    @classmethod
    def respond_request(cls, my_id, sender_id, accept):

        me = cls.get_raw(my_id)
        sender = cls.get_raw(sender_id)

        if accept:
            me.accept_request_from(sender)

        else:
            me.reject_request_from(sender)

        return {'message': 'OK'}, 200

    @classmethod
    def are_friends(cls, id1, id2):
        id1 = cls.get_raw(id1)
        id2 = cls.get_raw(id2)

        return id2 in id1.friends

    @classmethod
    def get_tkn(cls, id):
        return cls.get_raw(id).push_token

    @classmethod
    def set_tkn(cls, id, tkn):
        usr = cls.get_raw(id)
        usr.push_token = tkn

        db.session.commit()

    @classmethod
    def delete_tkn(cls, id):
        usr = cls.get_raw(id)
        usr.push_token = None

        db.session.commit()


