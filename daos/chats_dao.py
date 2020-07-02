from app import db
from models.msg_elements import Chat, Message

from services.usernotifier import UserNotifier, MessageTypes

import logging

class ChatsDAO():

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def get_messages_between(cls, uuid1, uuid2, page, per_page):

        minUID, maxUID = cls.sort_uuids(uuid1, uuid2)

        chat = Chat.query.get((minUID, maxUID))

        if chat:
            cls.logger().debug(f"Tipo de chat.messages: {type(chat.messages)}")

            cls.logger().info(f"Found chat between users {uuid1}, {uuid1}. Serializing...")
            return [m.serialize() for m in chat.messages]

        cls.logger().info(f"No messages found for users {uuid1}, {uuid2}")
        
        return []

    @classmethod
    def send_message(cls, sender_uuid, recver_uuid, text):

        minUID, maxUID = cls.sort_uuids(sender_uuid, recver_uuid)

        chat = Chat.query.get((minUID, maxUID))

        if not chat:
            cls.logger().info(f"No chat entry for users {sender_uuid}, {recver_uuid}. Adding entry...")
            chat = Chat(user1_id=minUID, user2_id=maxUID)
            db.session.add(chat)
            db.session.commit()

        new_msg = Message(sender_id=sender_uuid, recver_id=recver_uuid, text=text)
        new_msg.chat = chat

        db.session.add(new_msg)
        db.session.commit()

        cls.logger().info("Succesfully appended message to conversation")

        UserNotifier.send_notification(recver_uuid, "Nuevo mensaje sin leer", text, MessageTypes.MESSAGE.value, {"id":new_msg.id, "msg":text, "uuid": sender_uuid})

        return new_msg.serialize()




    @classmethod
    def sort_uuids(cls, u1, u2):
        return min(u1,u2), max(u1,u2)