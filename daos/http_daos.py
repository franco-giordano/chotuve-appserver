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
    def count_reqs_per_hour(cls):
        reqs = HTTPResponse.query.with_entities(extract('hour', HTTPResponse.timestamp).label('h'), func.count(HTTPResponse.id)).group_by('h').all()

        req_map = {}

        for r in reqs:
            req_map[r[0]] = r[1]

        return req_map
