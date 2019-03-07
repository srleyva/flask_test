from flask import Response
from flask_restplus import Resource
from prometheus_client import generate_latest

from api.v1.restplus import api

ns = api.namespace('system', description='Information about the API System')


@ns.route('/health')
class Health(Resource):
    @api.doc('get_health')
    def get(self):
        return {'message': 'System is healthy'}, 200


@ns.route('/metrics')
class Metrics(Resource):
    @api.doc('get_metrics')
    def get(self):
        CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
