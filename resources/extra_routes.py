from flask_restful import Resource, reqparse
import logging

from services.authsender import AuthSender

# /users/user_id/friends
class PingRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(PingRoute, self).__init__()

    def get(self):
        self.logger.info(f"Received PING request")

        return {'appserver':'UP'}, 200

# /auth
class AuthRoutes(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args_dict = parser.parse_args()
        
        id = AuthSender.get_uuid_from_token(args_dict["x-access-token"])

        return  {"id":id}, 200