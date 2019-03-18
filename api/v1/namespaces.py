import logging

from flask import Blueprint

from api.v1.restplus import api
from api.v1 import system, jobs

blueprint = Blueprint('api', __name__, url_prefix='/v1')
log = logging.getLogger(__name__)


def configure_api(job_queue):
    """
    Place to inject needed external dependencies
    the API may have

    :param job_queue: Hook to inject job_queue dependency
    :type job_queue: unittest.mock.Mock
    """

    jobs.job_queue = job_queue


api.init_app(blueprint)
api.add_namespace(system.ns)
api.add_namespace(jobs.ns)
