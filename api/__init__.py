import os
import logging.config

from flask import Flask
from flask_jwt_extended import JWTManager
from gevent.pywsgi import WSGIServer

from api import settings
from api.v1.namespaces import blueprint, configure_api
from api.databases import initialize_db

app = Flask(__name__)
jwt = JWTManager(app)

logging_conf_path = os.path.normpath(settings.LOGGING_CONF)
try:
    logging.config.fileConfig(logging_conf_path)
except KeyError:
    logging.warning('No logging config found')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    """
    Set configurations options for the Flask App

    :param flask_app: An instance of the app Instance
    :type flask_app: flask.Flask

    """

    flask_app.logger = log
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI # NOQA
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS # NOQA
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION # NOQA
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY


def initialize_app(flask_app, job_queue=None):
    """
    Set up the routes, db, models and injects needed
    dependencies

    :param flask_app: An instance of the app Instance
    :param job_queue: Hook to inject job_queue dependency
    :type flask_app: flask.Flask
    :type job_queue: unittest.mock.Mock
    """
    configure_api(job_queue)
    configure_app(flask_app)
    initialize_db(flask_app)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    log.info(f'Starting server at http://{settings.FLASK_SERVER_NAME}/v1')
    http_server = WSGIServer(('', 80), app, log=app.logger)
    http_server.serve_forever()


if __name__ == "__main__":
    main()
