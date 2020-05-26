from flask_restful import reqparse, Resource

from utils.decorators import token_required

# from daos.comments_dao import CommentDAO

from services.authsender import AuthSender


class AuthRoute(Resource):
    def __init__(self):
        super(AuthRoute, self).__init__()
        
    # TODO no hace nada
    def delete(self):
        return {'message':'Session ended'}, 200
        
    @token_required
    def post(self):
        return {'message': 'Valid token provided!'}, 201