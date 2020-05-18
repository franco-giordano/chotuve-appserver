import requests
import os


class MediaSender():

    url = 'http://' + os.environ['CH_MEDIASV_URL']

    @classmethod
    def send_url_to_mediasv(cls, vid_id,fb_url):
        r = requests.post(cls.url + '/video', data={'videoId': vid_id, 'url': fb_url})
        return r

    @classmethod
    def get_url_from_mediasv(cls,vid_id):
        r = requests.get(cls.url + '/video', data={'videoId': vid_id})

        if r.status_code != 200:
            return ''

        return r.json()['url']