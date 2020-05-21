from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
# from daos.comments_dao import CommentDAO

# from models.models import Comment

from utils.decorators import token_required

from services.authsender import AuthSender


parser = reqparse.RequestParser()
parser.add_argument("x-access-token", location='headers')


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
        args = parser.parse_args()
        uuid = AuthSender.get_uuid_from_token(args['x-access-token'])
        
        vids = VideoDAO.get_videos_by(user_id, uuid)

        return vids, 200
        

    