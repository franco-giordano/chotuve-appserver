
from flask_restful import Resource, reqparse

from daos.chats_dao import ChatsDAO
from daos.users_dao import UsersDAO

from services.authsender import AuthSender

from exceptions.exceptions import BadRequestError, UnauthorizedError

import logging


# /messages/<chat_with_uuid>
class MessagesRoute(Resource):
    
    def __init__(self):
        super(MessagesRoute, self).__init__()
        
    def get(self, other_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("page", location='args', type=int, required=True, help='Page number to retrieve messages')
        parser.add_argument("per_page", location='args', type=int, required=True, help='Amount of messages to download')
        
        args = parser.parse_args()

        uuid1 = AuthSender.get_uuid_from_token(args['x-access-token'])

        msgs = ChatsDAO.get_messages_between(uuid1, other_user_id)

        return msgs, 200

    def post(self, other_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help='Missing user token!')
        parser.add_argument("text", location='json', type=str, required=True, help='You must include the text to be sent!')
        
        args = parser.parse_args()

        if args["text"] == "":
            raise BadRequestError("Invalid message length")

        sender_uuid = AuthSender.get_uuid_from_token(args['x-access-token'])

        if not UsersDAO.are_friends():
            raise BadRequestError("You are not friends with this user")

        msg = ChatsDAO.send_message(sender_uuid, other_user_id, args["text"])

        return msg, 200
