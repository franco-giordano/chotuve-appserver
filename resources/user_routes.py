from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
# from daos.comments_dao import CommentDAO


from utils.decorators import token_required

from services.authsender import AuthSender

from daos.users_dao import FriendshipsDAO

from exceptions.exceptions import EndpointNotImplementedError


class UniqueUserRoute(Resource):
    def __init__(self):
        super(UniqueUserRoute, self).__init__()
        

    def get(self, user_id):

        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args = parser.parse_args()

        # TODO si hay datos privados, parsear viewer_uuid y pasarlo al authsv 
        msg, code = AuthSender.get_user_info(user_id, args['x-access-token'])

        return msg, code
        

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("display_name", location="json", required=False, type=str)
        parser.add_argument("email", location="json", required=False, type=str)
        parser.add_argument("phone_number", location="json", required=False,type=str)
        parser.add_argument("image_location", location="json", required=False, type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args_dict = parser.parse_args()
        args_dict = {k:v for k,v in args_dict.items() if v is not None}

        msg, code = AuthSender.modify_user(user_id ,args_dict)

        return msg, code


        
        


class UniqueUserVidsRoute(Resource):
    def __init__(self):
        super(UniqueUserVidsRoute, self).__init__()
        

    @token_required
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()
        uuid = AuthSender.get_uuid_from_token(args['x-access-token'])
        
        vids = VideoDAO.get_videos_by(user_id, uuid, args["x-access-token"])

        return vids, 200
        

class UsersRoute(Resource):
    def __init__(self):
        super(UsersRoute, self).__init__()


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("display_name", location="json", required=True, help="Missing user's full name.", type=str)
        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("phone_number", location="json", required=False, default="", type=str)
        parser.add_argument("image_location", location="json", required=False, default="", type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args = parser.parse_args()

        msg, code = AuthSender.register_user(fullname=args["display_name"], email=args['email'], phone=args['phone_number'],
            avatar=args['image_location'], token=args['x-access-token'])

        if code == 201:
            FriendshipsDAO.add_user_to_db(msg['id'])

        return msg, code

    # TODO /users?name=...
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument("name", type=str, required=False)
        parser.add_argument("email", type=str, required=False)
        parser.add_argument("phone", type=str, required=False)
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')

        args = parser.parse_args()

        msg, code = AuthSender.find_user(args["x-access-token"], args["name"], args["email"], args["phone"])

        return msg, code