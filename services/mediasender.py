import os

import logging

from utils.requester import Requester

import datetime


class MediaSender():

    url = os.environ['CH_MEDIASV_URL'] if os.environ['APP_SETTINGS'] != 'testing' else None

    mock_db = {}

    @classmethod
    def logger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def send_url(cls, vid_id, fb_url):
        if not cls.url:
            return cls._mock_send(vid_id, fb_url)
        
        payload = {'videoId': vid_id, 'url': fb_url}

        msg, code = Requester.media_fetch('POST', cls.url + '/videos', {}, payload)
        if code != 201:
            cls.logger().error(f"Error uploading video for ID: {vid_id}. Response: {msg}, code {code}")

        return msg['url'], msg['timestamp']


    @classmethod
    def get_info(cls, vid_id):

        if not cls.url:
            return cls._mock_get(vid_id)

        msg, code = Requester.media_fetch('GET', cls.url + '/videos/' + str(vid_id), {}, {})

        if code != 200:
            cls.logger().error(f"Error getting video info for ID: {vid_id}. Response: {msg}, code {code}")

        return msg['url'], msg['timestamp']

    @classmethod
    def delete_vid(cls, vid_id):
        if not cls.url:
            return cls.mock_db
        
        msg, code = Requester.media_fetch('DELETE', cls.url + '/videos/' + str(vid_id), {}, {})

        if code != 200:
            cls.logger().error(f"Error deleting video {vid_id}")

    @classmethod
    def _mock_send(cls, vid_id, fb_url):
        cls.mock_db[vid_id] = (fb_url, str(datetime.datetime.now(datetime.timezone.utc)))

        return fb_url, cls.mock_db[vid_id][1]

    @classmethod
    def _mock_get(cls, vid_id):
        vid_url, timestamp = cls.mock_db.get(vid_id)

        return vid_url, timestamp
