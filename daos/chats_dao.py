from app import db
from models.msg_elements import Chat, Message

from services.usernotifier import UserNotifier, MessageTypes

class ChatsDAO():
    
    @classmethod
    def get_messages_between(cls, uuid1, uuid2):

        minUID, maxUID = cls.sort_uuids(uuid1, uuid2)

        chat = Chat.query.get((minUID, maxUID))

        if chat:
            return [m.serialize() for m in chat.messages]
        
        return []

    @classmethod
    def send_message(cls, sender_uuid, recver_uuid, text):

        minUID, maxUID = cls.sort_uuids(sender_uuid, recver_uuid)

        chat = Chat.query.get((minUID, maxUID))

        if not chat:
            chat = Chat(user1_id=minUID, user2_id=maxUID)
            db.session.add(chat)
            db.session.commit()

        new_msg = Message(sender_id=sender_uuid, recver_id=recver_uuid, text=text)
        new_msg.chat = chat

        db.session.add(new_msg)
        db.session.commit()

        UserNotifier.send_notification(recver_uuid, "Nuevo mensaje sin leer", text, MessageTypes.MESSAGE.value, {"id":new_msg.id, "msg":text, "uuid": sender_uuid})

        return new_msg.serialize()




    @classmethod
    def sort_uuids(cls, u1, u2):
        return min(u1,u2), max(u1,u2)