from utils.decorators import token_required
from flask_restful import Resource

from daos.users_dao import FriendshipsDAO

import logging

# /users/user_id/friends
class FriendsRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(FriendsRoute, self).__init__()

    @token_required
    def get(self, user_id):
        self.logger.debug(f"Starting friends search for user {user_id}")

        return FriendshipsDAO.get_friends(user_id), 200

    @token_required
    def post(self, user_id):
        self.logger.debug(f"Starting friendship add for user {user_id}")

        return FriendshipsDAO.add_user(user_id), 201