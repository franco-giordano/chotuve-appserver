from utils.decorators import token_required
from flask_restful import Resource, reqparse

from daos.users_dao import FriendshipsDAO

from services.authsender import AuthSender

from exceptions.exceptions import EndpointNotImplementedError, BadRequestError

import logging

# TODO no usa friend requests! arreglar

# /users/user_id/friends
class FriendsRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(FriendsRoute, self).__init__()

    @token_required
    def get(self, user_id):
        self.logger.debug(f"Starting friends search for user {user_id}")

        return FriendshipsDAO.get_friends(user_id), 200


# /users/id/friends/requests
class RequestsRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(RequestsRoute, self).__init__()

    @token_required
    def get(self, user_id):

        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        sender_uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        if sender_uuid != user_id:
            raise BadRequestError("You can't view friend requests from someone else!")

        return FriendshipsDAO.view_pending_reqs(user_id), 200

    @token_required
    def post(self, user_id):

        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        sender_uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        msg, code = FriendshipsDAO.send_request(sender_uuid, user_id)

        return msg, code

# TODO aceptar/denegar requests!

# /users/myid/friends/requests/otherid
class UniqueRequestRoute(Resource):
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()

    @token_required
    def post(self, my_id, sender_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        parser.add_argument("accept", location='json', type=bool, required=True, help='You must specify if you either accept or reject the request')
        args = parser.parse_args()

        viewer_uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        if viewer_uuid != my_id:
            raise BadRequestError("You can't respond other user's friend requests!")

        msg, code = FriendshipsDAO.respond_request(my_id, sender_id, accept=args["accept"])

        return msg, code