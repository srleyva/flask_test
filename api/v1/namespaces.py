from flask import Blueprint

from api.v1.restplus import api
from api.v1 import system
from api.v1 import jobs

blueprint = Blueprint('api', __name__, url_prefix='/v1')


def configure_api(job_queue):
    '''Inject API Dependancies'''
    jobs.job_queue = job_queue


api.init_app(blueprint)
api.add_namespace(system.ns)
api.add_namespace(jobs.ns)
