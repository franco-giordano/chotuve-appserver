
from services.usernotifier import UserNotifier, MessageTypes

from services.authsender import AuthSender

MESSAGE_TITLE = "Nuevo mensaje sin leer"

REQUEST_TITLE = "Nueva solicitud de amistad"


class NotificationsCreator():

    @classmethod
    def notify_message(cls, sender_uuid, rcver_uuid, msg_id, msg_text, author_name):
        
        subtitle = author_name + ": " + msg_text
        UserNotifier.send_notification(recver_uuid, MESSAGE_TITLE, subtitle, MessageTypes.MESSAGE.value, {"id":msg_id, "msg":msg_text, "uuid": sender_uuid})


    @classmethod
    def notify_new_friend_req(cls, rcver_uuid, author_name):
        
        subtitle = f"Solicitud de {author_name}"
        UserNotifier.send_notification(rcver_uuid, REQUEST_TITLE, subtitle, MessageTypes.FRIEND_REQ.value, {})
