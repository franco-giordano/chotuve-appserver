from models.http_elements import HTTPResponse
from app import db

from sqlalchemy import extract, func


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
    def _tuple_to_map(cls, tuple_list):
        my_map = {}

        for t in tuple_list:
            my_map[t[0]] = t[1]

        return my_map