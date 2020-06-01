from flask_restful import Resource
import logging

# /users/user_id/friends
class PingRoute(Resource):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(PingRoute, self).__init__()

    def get(self):
        self.logger.info(f"Received PING request")

        return {'appserver':'UP'}, 200