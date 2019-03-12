from flask import Blueprint

from api.v1.restplus import api
from api.v1 import system, jobs

blueprint = Blueprint('api', __name__, url_prefix='/v1')


def configure_api(job_queue):
    '''Injects job_queue

    The only purpose is a hook to inject a mock

    Parameters
    ----------
    job_queue : api.services.job_queue.JobQueue
        None default to JobQueue
    '''

    jobs.job_queue = job_queue


api.init_app(blueprint)
api.add_namespace(system.ns)
api.add_namespace(jobs.ns)
