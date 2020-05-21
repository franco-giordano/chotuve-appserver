from flask_restful import reqparse, Resource

from services.mediasender import MediaSender
from services.authsender import AuthSender

from daos.videos_dao import VideoDAO
from daos.reactions_dao import ReactionDAO

from models.models import Video

from utils.decorators import token_required

# video_fields = {
#     'title': fields.String,
#     'description': fields.String,
#     'is_private': fields.Boolean,
#     'uuid': fields.Url('task'),
#     'location':fields.String,

# }

post_parser = reqparse.RequestParser()
post_parser.add_argument("x-access-token", location='headers')
post_parser.add_argument('description', type = str, default = "", location = 'json')
post_parser.add_argument('location', type = str, default = "", location = 'json')
post_parser.add_argument('title', type = str, default = "", location = 'json')
post_parser.add_argument('is-private', type = bool, default = False, location = 'json')
post_parser.add_argument('firebase-url', type = str, required = True, help="No firebase URL provided", location = 'json')



class UniqueVideoRoute(Resource):
    def __init__(self):
       super(UniqueVideoRoute, self).__init__()
        
    @token_required
    def get(self, vid_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        vid = VideoDAO.get(vid_id)

        vid['firebase-url'], vid['timestamp'] = MediaSender.get_info(vid_id)

        vid['reaction'] = ReactionDAO.reaction_by(vid_id, uuid)

        return vid, 200

    # TODO delete(cls)
        


class VideoRoute(Resource):
    def __init__(self):
        super(VideoRoute, self).__init__()
        
    @token_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        # TODO esto de uuid esta repetido en todos los route, ver como generalizar (decorator?)
        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        videos = VideoDAO.get_all()

        for video in videos:
            video['firebase-url'], video['timestamp'] = MediaSender.get_info(video['video_id'])
            video['reaction'] = ReactionDAO.reaction_by(video['video_id'], uuid)

        return videos, 200

    @token_required
    def post(self):
        args = post_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        # assign vid id
        new_vid = Video()

        # add to local db
        VideoDAO.add_vid(title=args['title'], description=args['description'], uuid=uuid, 
                        location=args['location'], is_private=args['is-private'])

        # upload to mediasv
        new_vid_with_url = new_vid.serialize()
        new_vid_with_url['firebase-url'], new_vid_with_url['timestamp'] = MediaSender.send_url(new_vid.id,args['firebase-url'])

        return new_vid_with_url, 201


