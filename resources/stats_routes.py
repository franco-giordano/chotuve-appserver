from flask_restful import Resource
from daos.http_daos import httpDAO


# /stats
class StatsRoutes(Resource):

    def get(self):

        count = httpDAO.count_total()

        requests_per_hour = httpDAO.count_reqs_per_hour()

        return {
            "requests_per_hour": requests_per_hour,
            "total_count": count
        }