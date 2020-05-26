import requests
import os

from flask_restful import abort

import logging

# from mockers.media_mocker import MediaMocker

class MediaSender():

    url = 'http://' + os.environ['CH_MEDIASV_URL'] #if os.environ['APP_SETTINGS'] == 'production' else None

    mock_db = {}

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)


    @classmethod
    def send_url(cls, vid_id,fb_url):
        if not cls.url:
            return cls._mock_send(vid_id, fb_url)

        r = requests.post(cls.url + '/video', data={'videoId': vid_id, 'url': fb_url})
        return r.json()['url'], r.json['timestamp']

    @classmethod
    def get_info(cls,vid_id):

        if not cls.url:
            return cls._mock_get(vid_id)

        cls.logger().info(f"Sending request to {cls.url}")

        r = requests.get(cls.url + '/video', data={'videoId': vid_id})

        # TODO manejar mejor los errores de conexion
        if r.status_code != 200:
            abort(500, message="Error contacting Media Server")

        return r.json()['url'], r.json()['timestamp']

    @classmethod
    def _mock_send(cls, vid_id, fb_url):
        cls.mock_db[vid_id] = fb_url

        return fb_url, "PREV_TIMESTAMP"

    @classmethod
    def _mock_get(cls, vid_id):
        vid_url = cls.mock_db.get(vid_id, "PREVIOUS_URL")

        return vid_url, "PREV_TIMESTAMP"
