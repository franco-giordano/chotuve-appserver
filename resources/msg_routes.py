
from flask_restful import Resource, reqparse

from daos.chats_dao import ChatsDAO
from daos.users_dao import UsersDAO

from services.authsender import AuthSender

from exceptions.exceptions import BadRequestError, UnauthorizedError

import logging


# /messages/<chat_with_uuid>
class MessagesRoute(Resource):
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(MessagesRoute, self).__init__()
        
    def get(self, other_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        args = parser.parse_args()

        uuid1 = AuthSender.get_uuid_from_token(args['x-access-token'])

        UsersDAO.check_exists(uuid1)
        UsersDAO.check_exists(other_user_id)
        
        msgs = ChatsDAO.get_messages_between(uuid1, other_user_id)

        self.logger.info(f"Found {len(msgs)} messages between users {uuid1, other_user_id}. RESPONSECODE:200")
        return msgs, 200

    def post(self, other_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("text", location='json', type=str, required=True, help='You must include the text to be sent!')
        
        args = parser.parse_args()

        if args["text"] == "":
            raise BadRequestError("Invalid message length")

        sender_uuid = AuthSender.get_uuid_from_token(args['x-access-token'])
        author_name = AuthSender.get_author_name(sender_uuid, args["x-access-token"])

        if not UsersDAO.are_friends(sender_uuid, other_user_id):
            raise BadRequestError("You are not friends with this user")

        msg = ChatsDAO.send_message(sender_uuid, other_user_id, args["text"], author_name)

        self.logger.info(f"Succesfully sent message from user {sender_uuid} to {other_user_id}. RESPONSECODE:200")
        return msg, 201
