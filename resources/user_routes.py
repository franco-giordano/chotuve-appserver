from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
# from daos.comments_dao import CommentDAO


from utils.decorators import token_required

from services.authsender import AuthSender

from daos.users_dao import UsersDAO

from exceptions.exceptions import BadRequestError

import logging

class UniqueUserRoute(Resource):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(UniqueUserRoute, self).__init__()
        

    def get(self, user_id):

        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args = parser.parse_args()

        msg, code = AuthSender.get_user_info(user_id, args['x-access-token'])

        if code==200:
            viewer_id = AuthSender.get_uuid_from_token(args["x-access-token"])
            msg["friendship_status"] = UsersDAO.get_friendship_status(user_id, viewer_id)

        self.logger.info(f"User {user_id} info collected: {msg}. RESPONSECODE:{code}")
        return msg, code
        

    def patch(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("display_name", location="json", required=False, type=str)
        parser.add_argument("email", location="json", required=False, type=str)
        parser.add_argument("phone_number", location="json", required=False,type=str)
        parser.add_argument("image_location", location="json", required=False, type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("password", location="json", required=False, default="", type=str)

        args_dict = parser.parse_args()
        args_dict = {k:v for k,v in args_dict.items() if v is not None}

        msg, code = AuthSender.modify_user(user_id ,args_dict)

        self.logger.info(f"User {user_id} info edited: {msg}. RESPONSECODE:{code}")
        return msg, code

    def delete(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args = parser.parse_args()

        viewer_uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        if not AuthSender.has_permission(user_id, viewer_uuid):
            self.logger.info(f"User {viewer_uuid} attempted to delete user's {user_id} account. Access Denied.")
            raise BadRequestError(f"You can't delete other users profiles!")

        UsersDAO.delete_user(user_id, args["x-access-token"])

        return {"message":"OK"}, 200


        


class UniqueUserVidsRoute(Resource):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(UniqueUserVidsRoute, self).__init__()
        

    @token_required
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()
        viewer_uuid = AuthSender.get_uuid_from_token(args['x-access-token'])
        
        vids = VideoDAO.get_videos_by(user_id, viewer_uuid, args["x-access-token"])

        self.logger.info(f"{len(vids)} vids collected by user {user_id}. RESPONSECODE:200")
        return vids, 200
        

class UsersRoute(Resource):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(UsersRoute, self).__init__()


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("display_name", location="json", required=True, help="Missing user's full name.", type=str)
        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("phone_number", location="json", required=False, default="", type=str)
        parser.add_argument("image_location", location="json", required=False, default="", type=str)
        parser.add_argument("password", location="json", required=False, default="", type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args = parser.parse_args()

        msg, code = AuthSender.register_user(fullname=args["display_name"], email=args['email'], phone=args['phone_number'],
            avatar=args['image_location'],token=args['x-access-token'], password=args["password"])

        if code == 201:
            self.logger.info(f"New user created with info: {msg}. RESPONSECODE:{code}")
            UsersDAO.add_user_to_db(msg['id'])
        else:
            self.logger.error(f"Failed to create user with info: {msg}. RESPONSECODE:{code}")

        return msg, code


    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument("name", type=str, required=False, location='args')
        parser.add_argument("email", type=str, required=False, location='args')
        parser.add_argument("phone", type=str, required=False, location='args')

        parser.add_argument('per_page', type=int, required=False, location='args')
        parser.add_argument('page', type=int, required=False, location='args')

        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args = parser.parse_args()

        msg, code = AuthSender.find_user(args["x-access-token"], args["name"], args["email"], args["phone"], args["per_page"], args["page"])
        
        self.logger.info(f"Executed user search with args name={args['name']}, email={args['email']}, phone={args['phone']}, per_page={args['per_page']}, page={args['page']}. RESPONSECODE:{code}")
        return msg, code


class UsersAdmin(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(UsersAdmin, self).__init__()

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args = parser.parse_args()

        msg, code = AuthSender.is_admin(args["x-access-token"])
        
        self.logger.info(f"Executed GET on /users/admin. Result: {msg['admin']} RESPONSECODE:{code}")
        return msg, code