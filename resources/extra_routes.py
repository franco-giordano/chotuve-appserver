from flask_restful import Resource, reqparse
import logging

from services.authsender import AuthSender

from daos.users_dao import UsersDAO

# /users/user_id/friends
class PingRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(PingRoute, self).__init__()

    def get(self):
        self.logger.info(f"Incoming PING request. RESPONSECODE:200")

        return {'appserver':'UP'}, 200

# /auth
class AuthRoutes(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args_dict = parser.parse_args()
        
        id = AuthSender.get_uuid_from_token(args_dict["x-access-token"])

        self.logger.info(f"Responding ID query for user {id}. RESPONSECODE:200")
        return  {"id":id}, 200


# /tokens
class PushTokensRoutes(Resource):

    def ___init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args_dict = parser.parse_args()
        
        id = AuthSender.get_uuid_from_token(args_dict["x-access-token"])
        self.logger.info(f"Returning push token for user {id}. RESPONSECODE:200")
        return { "push_token": UsersDAO.get_tkn(id) }, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("push_token", location='json', required=True, help="Missing Expo Push Token")
        args_dict = parser.parse_args()
        
        id = AuthSender.get_uuid_from_token(args_dict["x-access-token"])

        UsersDAO.set_tkn(id, args_dict["push_token"])

        self.logger.info(f"Added new push token for user {id}. RESPONSECODE:200")
        return {"message":"OK"}, 200

