from models.http_elements import HTTPResponse
from app import db

from sqlalchemy import extract, func

from datetime import datetime, timedelta


class httpDAO():

    @classmethod
    def add_entry(cls, path, method, response_code, client_ip):
        entry = HTTPResponse(path=path,
                            method=method,
                            response_code=response_code,
                            client_ip=client_ip)

        db.session.add(entry)
        db.session.commit()

    @classmethod
    def count_total(cls):
        return HTTPResponse.query.count()


    @classmethod
    def count_reqs_per_response_code(cls):
        reqs = HTTPResponse.query.with_entities(HTTPResponse.response_code, func.count(HTTPResponse.id)).group_by(HTTPResponse.response_code).all()

        return cls._tuple_to_map(reqs)

    @classmethod
    def count_reqs_per_method(cls):
        reqs = HTTPResponse.query.with_entities(HTTPResponse.method, func.count(HTTPResponse.id)).group_by(HTTPResponse.method).all()

        return cls._tuple_to_map(reqs)


    @classmethod
    def count_reqs_per_hour(cls):
        reqs = HTTPResponse.query.with_entities(extract('hour', HTTPResponse.timestamp).label('h'), func.count(HTTPResponse.id)).group_by('h').all()

        return cls._tuple_to_map(reqs)

    @classmethod
    def count_registered_users_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        users = HTTPResponse.query\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)\
                            .filter(HTTPResponse.path.contains('users'))\
                            .filter(HTTPResponse.method.contains('POST'))\
                            .with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        return cls._tuple_to_map(users)

    @classmethod
    def count_uploaded_vids_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        vids = HTTPResponse.query\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)\
                            .filter(HTTPResponse.method.contains('POST'))\
                            .filter(HTTPResponse.path == '/videos')\
                            .with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        return cls._tuple_to_map(vids)

    @classmethod
    def count_posted_comments_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        vids = HTTPResponse.query\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)\
                            .filter(HTTPResponse.method.contains('POST'))\
                            .filter(HTTPResponse.path.contains('comments'))\
                            .with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        return cls._tuple_to_map(vids)

    @classmethod
    def count_requests_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        reqs = HTTPResponse.query\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)\
                            .with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        return cls._tuple_to_map(reqs)

    @classmethod
    def count_sv_errors_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)
        query = HTTPResponse.query\
                            .filter(HTTPResponse.response_code >= 500)\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)
                            
        reqs = query.with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        reqs_per_path = query.with_entities(HTTPResponse.method, HTTPResponse.path, func.count(HTTPResponse.id))\
                            .group_by(HTTPResponse.method, HTTPResponse.path).all()

        return cls._tuple_to_map(reqs), cls._double_tuple_to_map(reqs_per_path)

    @classmethod
    def count_cli_errors_in_30_days(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        query = HTTPResponse.query\
                            .filter(HTTPResponse.response_code >= 400)\
                            .filter(HTTPResponse.response_code < 500)\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)
                            
                            
        reqs = query.with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        reqs_per_path = query.with_entities(HTTPResponse.method, HTTPResponse.path, func.count(HTTPResponse.id))\
                            .group_by(HTTPResponse.method, HTTPResponse.path).all()

        return cls._tuple_to_map(reqs), cls._double_tuple_to_map(reqs_per_path)

    @classmethod
    def count_views_per_day(cls):
        current_time = datetime.utcnow()

        thirty_days_ago = current_time - timedelta(days=30)

        vids = HTTPResponse.query\
                            .filter(HTTPResponse.timestamp > thirty_days_ago)\
                            .filter(HTTPResponse.method.contains('GET'))\
                            .filter(HTTPResponse.path.contains('comments'))\
                            .with_entities(extract('day', HTTPResponse.timestamp).label('d'), func.count(HTTPResponse.id))\
                            .group_by('d').all()

        return cls._tuple_to_map(vids)

    @classmethod
    def _tuple_to_map(cls, tuple_list):
        my_map = {}

        for t in tuple_list:
            my_map[t[0]] = t[1]

        return my_map

    

    @classmethod
    def _double_tuple_to_map(cls, tuple_list):
        my_map = {}

        for t in tuple_list:
            my_map[t[0] + " " + t[1]] = t[2]

        return my_map