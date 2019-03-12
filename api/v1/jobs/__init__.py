from flask import jsonify
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from api.v1.restplus import api
from api.models.data_engine_job import DataEngineJob, JobSchema
from api.services.job_queue import JobQueue
from api.services.source_tree import AccountSourceTree

ns = api.namespace('jobs', description='Job Related information')
parser = ns.parser()
parser.add_argument(
    'Authorization',
    type=str,
    location='headers',
    help='Bearer Access Token',
    required=True)

job_queue = None
account_tree = AccountSourceTree
data_engine_job = DataEngineJob()


@ns.route('/')
class JobsCollection(Resource):
    @jwt_required
    @ns.doc(parser=parser)
    @api.doc('peek')
    @api.response(404, 'No Jobs in Queue')
    def get(self):
        '''Peek at the top Job'''
        next_job = queue(job_queue).peek()
        if next_job is None:
            self.api.abort(
                404,
                f'No Jobs in queue'
            )
        return jsonify(JobSchema().dump(next_job).data)

    @jwt_required
    @ns.doc(parser=parser)
    @api.doc('refresh')
    @api.response(404, 'No Jobs in Queue')
    def put(self):
        '''Refresh the Jobs Queue'''
        queue(job_queue).refresh()
        return {'success': 'true'}, 200

    @jwt_required
    @ns.doc(parser=parser)
    @api.doc('pop')
    def delete(self):
        '''Pop a Job off of the job queue'''
        next_job = queue(job_queue).pop()
        if next_job is None:
            self.api.abort(
                404,
                f'No Jobs in queue'
            )
        return jsonify(JobSchema().dump(next_job).data)


@ns.route('/<int:job_id>')
@api.response(404, 'Job Not Found')
class JobsItems(Resource):
    @jwt_required
    @ns.doc(parser=parser)
    @api.response(404, 'Job not found.')
    def get(self, job_id):
        '''Get job information'''
        job = data_engine_job.query.get(job_id)
        if job is None:
            self.api.abort(
                404,
                f'Job not found {job_id}'
            )
        return jsonify(JobSchema().dump(job).data)

    @jwt_required
    @ns.doc(parser=parser)
    @api.response(200, 'Job successfully deleted.')
    @api.response(404, 'Job not found.')
    def delete(self, job_id):
        '''Delete a job'''
        job = data_engine_job.query.get(job_id)
        if job is None:
            self.api.abort(
                404,
                f'Job not found {job_id}'
            )
        queue(job_queue).remove(job)
        return {'success': 'true'}, 200


@ns.route('/<int:job_id>/priority/<int:priority>')
class JobPriority(Resource):
    @jwt_required
    @ns.doc(parser=parser)
    @api.response(200, 'Job successfully updated.')
    @api.response(404, 'Job not found.')
    def put(self, job_id, priority):
        '''Set the priority of job'''
        job = data_engine_job.query.get(job_id)
        if job is None:  # pragma: no cover
            self.api.abort(
                404,
                f'Job not found {job_id}'
            )
        job.priority = priority
        queue(job_queue).set(job)
        return {"success": "true"}, 200


@ns.route('/<int:account_id>/source_tree')
class JobSourceTree(Resource):
    @jwt_required
    @ns.doc(parser=parser)
    def get(self, account_id):
        '''Get Source tree for particular account'''
        tree = account_tree(account_id)
        tree.refresh()
        return jsonify(tree.data)


def queue(job_queue):  # pragma: no cover
    if job_queue is None:
        job_queue = JobQueue()
    return job_queue
