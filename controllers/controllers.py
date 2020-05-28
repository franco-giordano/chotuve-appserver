from flask import make_response, jsonify
from flask_restful import Api
from run import app

# import requests, os

from resources.videos_routes import VideoRoute, UniqueVideoRoute
from resources.comments_routes import CommentRoute
from resources.reactions_route import ReactionRoute
from resources.user_routes import UniqueUserRoute, UniqueUserVidsRoute, UsersRoute
from resources.auth_route import AuthRoute
from resources.friends_routes import FriendsRoute

api = Api(app)

import logging
logger = logging.getLogger(__name__)
api.add_resource(VideoRoute, '/videos')
api.add_resource(UniqueVideoRoute, '/videos/<int:vid_id>')
api.add_resource(CommentRoute, '/videos/<int:vid_id>/comments')
api.add_resource(ReactionRoute, '/videos/<int:vid_id>/reactions')

api.add_resource(UniqueUserRoute, '/users/<int:user_id>')
api.add_resource(UniqueUserVidsRoute, '/users/<int:user_id>/videos')
api.add_resource(UsersRoute, '/users')

# api.add_resource(FriendsRoute, '/users/<int:user_id>/friends')


# endpoints faltantes:
# TODO users endpoint (buscar info de uno, vids de uno) [WIP]
# TODO recuperar password
# TODO ingresar nueva password
# TODO agregar amigos
# TODO chat (???)
# TODO stats

@app.route('/ping', methods=['GET'])
def status():
    return jsonify({'appserver':'UP'})



# # @app.route('/video/<id>', methods=['DELETE'])
# # def delete_single_vid(id):
# #     vid = Video.query.get(id)

# #     db.session.delete(vid)
# #     db.session.commit()

# #     return video_schema.jsonify(vid)


# @app.route('/')
# def hi():
#     url = 'http://'+ os.environ['CH_MEDIASV_URL'] + '/'
#     logger.debug(f"requesting for {url}")
#     r = requests.get(url)

#     return jsonify({"message":f"response {r.status_code}"}), r.status_code