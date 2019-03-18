import logging

from flask import Response
from flask_restplus import Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, get_raw_jwt,
    create_refresh_token
)
from sqlalchemy.sql import text
from prometheus_client import generate_latest

from api.v1.restplus import api
from api.databases import db

log = logging.getLogger(__name__)

ns = api.namespace('system', description='Information about the API System')
pg_db = db
parser = ns.parser()
parser.add_argument(
    'Authorization',
    type=str,
    location='headers',
    help='Bearer Access Token',
    required=True)

health_model = ns.model('health', {
    'database': fields.Boolean,
    'application': fields.Boolean,
    'ready': fields.Boolean,
})

token_model = ns.model('token', {
    'token': fields.String,
    'refresh': fields.String,
})


@ns.route('/token')
class Token(Resource):
    """This handles method on the JWT token

    This class will generate and parse JWT tokens
    passed from the client
    """
    @api.doc('create_token')
    @ns.marshal_with(token_model)
    def get(self):
        """
        Generates a JWT and refresh token

        :return: token_model
        """
        access_token = create_access_token("temp-system")
        refresh_token = create_refresh_token("temp-system")
        tokens = {
            "token": access_token,
            "refresh": refresh_token,
        }
        return tokens, 200

    @api.doc('token_info')
    @jwt_required
    @ns.doc(parser=parser)
    def post(self):
        """
        Parses claims from the JWT

        :return: dict
        """
        claims = get_raw_jwt()
        return claims, 200


@ns.route('/health')
class Health(Resource):
    @api.doc('get_health')
    @ns.marshal_with(health_model)
    def get(self):
        """
        Check the health of the system
        and returns to client

        Check the health of the DB and API

        :return: health, http status code
        :rtype: api.v1.system.health_model, int
        """
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
        """
        Generates and returns Prometheus metrics

        :return: flask.Response
        """
        CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
