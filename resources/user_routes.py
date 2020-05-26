from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
# from daos.comments_dao import CommentDAO


from utils.decorators import token_required

from services.authsender import AuthSender




class UniqueUserRoute(Resource):
    def __init__(self):
        super(UniqueUserRoute, self).__init__()
        

    @token_required
    def get(self, user_id):

        # TODO si hay datos privados, parsear viewer_uuid y pasarlo al authsv 
        user = AuthSender.get_user_info(user_id)

        return user, 200
        
    @token_required
    def put(self, user_id):
        # TODO edit my info
        pass


class UniqueUserVidsRoute(Resource):
    def __init__(self):
        super(UniqueUserVidsRoute, self).__init__()
        

    @token_required
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()
        uuid = AuthSender.get_uuid_from_token(args['x-access-token'])
        
        vids = VideoDAO.get_videos_by(user_id, uuid)

        return vids, 200
        
class UsersRoute(Resource):
    def __init__(self):
        super(UsersRoute, self).__init__()


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("fullname", location="json", required=True, help="Missing user's full name.", type=str)
        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("login-method", location="json", required=True,
            choices=('email', 'facebook', 'google'), help='Bad choice: {error_msg}', type=str)

        args = parser.parse_args()

        msg, code = AuthSender.register_user(fullname=args["fullname"], email=args['email'], method=args['login-method'])

        return msg, code
    