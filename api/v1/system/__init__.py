import logging

from flask import Response
from flask_restplus import Resource, fields
from flask_jwt_extended import create_access_token
from sqlalchemy.sql import text
from prometheus_client import generate_latest

from api.v1.restplus import api
from api.databases import db

ns = api.namespace('system', description='Information about the API System')
pg_db = db

health_model = ns.model('health', {
    'database': fields.Boolean,
    'application': fields.Boolean,
    'ready': fields.Boolean,
})


@ns.route('/token')
class Token(Resource):
    @api.doc('create_token')
    def get(self):
        access_token = create_access_token("temp-system")
        return {'token': access_token}, 200


@ns.route('/health')
class Health(Resource):
    @api.doc('get_health')
    @ns.marshal_with(health_model)
    def get(self):
        status_code = 200
        database = True
        application = True
        try:
            pg_db.session.execute(text('SELECT 1'))
        except Exception as e:
            logging.warning(f'Database offline: {e}')
            database = False

        ready = application and database
        if not ready:
            status_code = 500
        health = {
            'database': database,
            'application': application,
            'ready': ready
        }
        return health, status_code


@ns.route('/metrics')
class Metrics(Resource):
    @api.doc('get_metrics')
    def get(self):
        CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
