from utils.decorators import token_required
from flask_restful import Resource, reqparse

from daos.users_dao import UsersDAO

from services.authsender import AuthSender

from exceptions.exceptions import EndpointNotImplementedError, BadRequestError, UnauthorizedError

import logging


# /users/user_id/friends
class FriendsRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(FriendsRoute, self).__init__()

    @token_required
    def get(self, user_id):
        self.logger.debug(f"Starting friends search for user {user_id}")
        friends = UsersDAO.get_friends(user_id)

        self.logger.info(f"Found {len(friends['friends'])} friend(s) for user {user_id}. RESPONSECODE:200")
        return friends, 200


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
            raise UnauthorizedError("You can't view other user's friend requests!")
        
        reqs = UsersDAO.view_pending_reqs(user_id)

        self.logger.info(f"Found {len(reqs['pending_reqs'])} pending requests for user {user_id}. RESPONSECODE:200")
        return reqs, 200

    @token_required
    def post(self, user_id):

        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        sender_uuid = AuthSender.get_uuid_from_token(args["x-access-token"])
        author_name = AuthSender.get_author_name(sender_uuid, args["x-access-token"])

        msg = UsersDAO.send_request(sender_uuid, user_id, author_name)

        self.logger.info(f"Succesfully sent request from user {sender_uuid} to {user_id}. RESPONSECODE:201")
        return msg, 201


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
            raise UnauthorizedError("You can't respond other user's friend requests!")

        msg = UsersDAO.respond_request(my_id, sender_id, accept=args["accept"])

        self.logger.info(f"User {my_id} responded request from {sender_id}. Accepted: {args['accept']}. RESPONSECODE:200")
        return msg, 200