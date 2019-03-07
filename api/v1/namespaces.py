from flask import Blueprint

from api.v1.restplus import api
from api.v1.system import ns as system_namespace
from api.v1.jobs import ns as job_namespace

blueprint = Blueprint('api', __name__, url_prefix='/v1')

api.init_app(blueprint)
api.add_namespace(system_namespace)
api.add_namespace(job_namespace)
