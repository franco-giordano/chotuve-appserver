from flask_restful import reqparse, Resource

from daos.videos_dao import VideoDAO
from daos.comments_dao import CommentDAO

from models.video_elements import Comment

from utils.decorators import token_required

from services.authsender import AuthSender

import logging

postcmnt_parser = reqparse.RequestParser()
postcmnt_parser.add_argument("x-access-token", location='headers')
postcmnt_parser.add_argument('text', type = str, required=True, help="Missing comment text!",location = 'json')
postcmnt_parser.add_argument('vid_time', type = str, required=False, location = 'json')       



class CommentRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(CommentRoute, self).__init__()
        

    @token_required
    def get(self, vid_id):
        comments = CommentDAO.get_all_from(vid_id)
        self.logger.info(f"Found all comments for vid {vid_id}. RESPONSECODE:200")
        return comments, 200

    @token_required
    def post(self, vid_id):
        args = postcmnt_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])
        new_cmnt = CommentDAO.add_cmnt(vid_id, uuid=uuid, text=args['text'], time=args["vid_time"], tkn=args["x-access-token"])

        self.logger.info(f"Posted new comment to video {vid_id}. Comment: {new_cmnt}. RESPONSECODE:201")
        return new_cmnt, 201
