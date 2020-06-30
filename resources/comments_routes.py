from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
from daos.comments_dao import CommentDAO

from models.video_elements import Comment

from utils.decorators import token_required

from services.authsender import AuthSender


postcmnt_parser = reqparse.RequestParser()
postcmnt_parser.add_argument("x-access-token", location='headers')
postcmnt_parser.add_argument('text', type = str, required=True, help="Missing comment text!",location = 'json')
postcmnt_parser.add_argument('vid_time', type = str, required=False, location = 'json')       



class CommentRoute(Resource):
    def __init__(self):
        super(CommentRoute, self).__init__()
        

    @token_required
    def get(self, vid_id):
        comments = CommentDAO.get_all_from(vid_id)
        return comments, 200

    @token_required
    def post(self, vid_id):
        args = postcmnt_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        new_cmnt = CommentDAO.add_cmnt(vid_id, uuid=uuid, text=args['text'], time=args["vid_time"])

        return new_cmnt, 201

    # TODO delete