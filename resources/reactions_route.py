from flask_restful import reqparse, Resource

from utils.decorators import token_required

from services.authsender import AuthSender

from daos.reactions_dao import ReactionDAO

import logging


class ReactionRoute(Resource):
    def __init__(self):
        self.rctn_parser = reqparse.RequestParser()
        self.rctn_parser.add_argument('x-access-token',location='headers')
        self.rctn_parser.add_argument('likes_video', type = bool, required=True, 
            help="No reaction provided." ,location = 'json')
        self.logger = logging.getLogger(self.__class__.__name__)
        super(ReactionRoute, self).__init__()
        
    @token_required
    def get(self, vid_id):
        reactions = ReactionDAO.get_all_from(vid_id)
        self.logger.info(f"Returning all reactions for vid {vid_id}. RESPONSECODE:200")
        return reactions, 200

    @token_required
    def post(self, vid_id):
        args = self.rctn_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        new_rctn = ReactionDAO.add_rctn(vid_id, uuid=uuid, likes=args['likes_video'])

        self.logger.info(f"Posted new reaction to vid {vid_id}. Is a like: {args['likes_video']} by {uuid}. RESPONSECODE:201")
        return new_rctn, 201


    @token_required
    def patch(self, vid_id):
        args = self.rctn_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        edited_rctn = ReactionDAO.edit_rctn(vid_id, uuid=uuid, likes=args['likes_video'])

        self.logger.info(f"Edited reaction to vid {vid_id}. Is a like: {args['likes_video']} by {uuid}. RESPONSECODE:201")
        return edited_rctn, 200

