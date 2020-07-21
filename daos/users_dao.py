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

        cls.logger().info(f"Added new friendship between users {rcv_id} and {sender_id}")

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
        cls.logger().debug(f"Creating new database entry for user {user_id} on friendships table")
        try:
            new_user = User(id=user_id)
            db.session.add(new_user)
            db.session.commit()
        except (UniqueViolation, IntegrityError) as e:
            cls.logger().error(f"Error when creating entry. Error: {e}")
            raise InternalError(f"User already exists with ID {user_id}")

        return new_user

    @classmethod
    def add_user_to_db(cls, user_id):
        cls.create_raw(user_id)

    @classmethod
    def send_request(cls, snd_id, rcv_id, author_name):
        cls.logger().info(f"send_request: checking it's a valid request... (step 1 - no self-invitations)")
        if snd_id == rcv_id:
            raise BadRequestError(
                "You can't send a friend request to yourself!")

        snd = cls.get_raw(snd_id)
        rcv = cls.get_raw(rcv_id)

        cls.logger().info(f"send_request: checking it's a valid request... (step 2 - no friends and can't spam requests)")
        if rcv.received_request_from(snd) or snd.is_friend_with(rcv):
            raise BadRequestError(
                f"You already sent a request, or are already friends.")


        cls.logger().info(f"send_request: checking it's a valid request... (step 3 - no pending request from other user)")
        if snd.received_request_from(rcv):
            raise BadRequestError(
                f"You have a pending request from this user, try accepting or rejecting it first.")

        snd.sent_requests.append(rcv)
        db.session.commit()

        cls.logger().debug(f"Sent requests: {snd.serializeSentReqs()}")
        cls.logger().debug(f"Received reqs: {rcv.serializeReceivedReqs()}")

        cls.logger().info(f"send_request: saved request succesfully from user {snd_id} to {rcv_id}")

        from services.notifications_creator import NotificationsCreator
        NotificationsCreator.notify_new_friend_req(rcv_id, author_name)

        return snd.serializeSentReqs()

    @classmethod
    def view_pending_reqs(cls, user_id):
        user = cls.get_raw(user_id)
        cls.logger().info(f"Grabbing pending reqs for user {user_id}...")

        return user.serializeReceivedReqs()

    @classmethod
    def respond_request(cls, my_id, sender_id, accept):

        me = cls.get_raw(my_id)
        sender = cls.get_raw(sender_id)

        if accept:
            me.accept_request_from(sender)
            cls.logger().info(f"User {my_id} accepted the request from {sender_id}")

        else:
            me.reject_request_from(sender)
            cls.logger().info(f"User {my_id} rejected the request from {sender_id}")

        return {'message': 'OK'}

    @classmethod
    def are_friends(cls, uuid1, uuid2):
        id1 = cls.get_raw(uuid1)
        id2 = cls.get_raw(uuid2)

        cls.logger().info(f"Checking if users {uuid1} and {uuid2} are friends...")
        return id2 in id1.friends


    @classmethod
    def already_pending_request(cls, u1, u2):
        user1 = cls.get_raw(u1)
        user2 = cls.get_raw(u2)

        if user1.received_request_from(user2) or user2.received_request_from(user1):
            cls.logger().info(f"Users {u1}, {u2} already have pending requests with each other")
            return True

        cls.logger().info(f"Users {u1}, {u2} dont have any pending requests with each other")
        return False

    @classmethod
    def delete_friendship(user_id, friend_id):

        if cls.are_friends(user_id, friend_id):
            user = cls.get_raw(user_id)
            friend = cls.get_raw(friend_id)

            user.delete_friendship(friend)
        else:
            raise NotFoundError(f"Friendship between users {user_id} and {friend_id} not found")


            

    @classmethod
    def get_tkn(cls, id):
        return cls.get_raw(id).push_token

    @classmethod
    def set_tkn(cls, id, tkn):
        user = User.query.filter_by(push_token=tkn).all()
        for u in user:
            u.push_token = None

        usr = cls.get_raw(id)
        usr.push_token = tkn

        db.session.commit()
        cls.logger().info(f"Set new push token for {id}. Token: {tkn}")

    @classmethod
    def delete_tkn(cls, id):
        usr = cls.get_raw(id)
        usr.push_token = None

        db.session.commit()
        cls.logger().warn(f"Deleted push token for {id}")

    @classmethod
    def get_friendship_status(cls, uuid1, uuid2):
        if cls.are_friends(uuid1, uuid2):
            return 'accepted'

        if cls.already_pending_request(uuid1, uuid2):
            return 'pending'

        return 'unknown'

