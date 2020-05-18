import requests
import os

class AuthSender():

    url = os.environ['CH_AUTHSV_URL']

    @classmethod
    def is_valid_token(cls, token):
        # r = requests.post(cls.url + '/video', data={'videoId': vid_id, 'url': fb_url})

        return True