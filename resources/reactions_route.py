from flask_restful import reqparse, Resource

from utils.decorators import token_required

from services.authsender import AuthSender

from daos.reactions_dao import ReactionDAO



class ReactionRoute(Resource):
    def __init__(self):
        self.rctn_parser = reqparse.RequestParser()
        self.rctn_parser.add_argument('x-access-token',location='headers')
        self.rctn_parser.add_argument('likes_video', type = bool, required=True, 
            help="No reaction provided." ,location = 'json')
        super(ReactionRoute, self).__init__()
        

    # TODO asi todas las reacciones son publicas, quitar de otro modo
    @token_required
    def get(self, vid_id):
        reactions = ReactionDAO.get_all_from(vid_id)
        return reactions, 200

    @token_required
    def post(self, vid_id):
        args = self.rctn_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        new_rctn = ReactionDAO.add_rctn(vid_id, uuid=uuid, likes=args['likes_video'])

        return new_rctn, 201

    # TODO delete
