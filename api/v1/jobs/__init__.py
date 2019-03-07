from flask import jsonify
from flask_restplus import Resource

from api.v1.restplus import api
from api.models.data_engine_job import DataEngineJob, JobSchema
from api.services.job_queue import JobQueue
from api.services.source_tree import AccountSourceTree

ns = api.namespace('jobs', description='Job Related information')


@ns.route('/')
class JobsCollection(Resource):
    @api.doc('peek')
    def get(self):
        '''Peek at the top Job'''
        next_job = JobQueue().peek()
        return jsonify(JobSchema().dump(next_job).data), 200

    @api.doc('refresh')
    def put(self):
        '''Refresh the Jobs Queue'''
        JobQueue.refresh()
        return {'success': 'true'}, 200

    @api.doc('pop')
    def delete(self):
        '''Pop a Job off of the job queue'''
        next_job = JobQueue().pop()
        return jsonify(JobSchema().dump(next_job).data), 200


@ns.route('/<int:job_id>')
@api.response(404, 'Job Not Found')
class JobsItems(Resource):
    def get(self, job_id):
        '''Get job information'''
        job = DataEngineJob.query.get(job_id)
        return jsonify(JobSchema.dump(job).data), 200

    @api.response(204, 'Job successfully deleted.')
    def delete(self, job_id):
        '''Delete a job'''
        job = DataEngineJob.query.get(job_id)
        JobQueue().remove(job)
        return {'success': 'true'}, 204


@ns.route('<int:job_id>/priority/<int:priority>')
class JobPriority(Resource):
    @api.response(204, 'Job successfully updated.')
    def put(self, job_id, priority):
        '''Set the priority of job'''
        job = DataEngineJob.query.get(job_id)
        job.priority = priority
        JobQueue().set(job)
        return {"success": "true"}, 200


@ns.route('/<int:account_id>/source_tree')
class JobSourceTree(Resource):
    def get(self, account_id):
        '''Get Source tree for particular account'''
        tree = AccountSourceTree(account_id)
        tree.refresh()
        return jsonify(tree.data), 200
