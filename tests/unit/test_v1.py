"""Unit tests for the Jobs API v1 Service endpoint"""
from datetime import datetime
import json
import unittest
from unittest.mock import Mock

import api
from api.services.job_queue import JobQueue
from api.models.data_engine_job import DataEngineJob
from api.services.source_tree import AccountSourceTree

mock_job_queue = Mock(JobQueue)
api.initialize_app(api.app, mock_job_queue)

test_job = DataEngineJob()
test_job.created_at = datetime.now()
test_job.priority = 2
test_job.state = "running"


class V1ServiceTest(unittest.TestCase):
    '''Tests for the V1 endpoints'''
    def setUp(self):
        '''Set some state for each test in this class'''
        api.app.testing = True
        self.app = api.app.test_client()
        self.mock_job_queue = mock_job_queue
        self.mock_data_engine = Mock(DataEngineJob)
        self.mock_account_tree = Mock(AccountSourceTree)
        api.v1.jobs.data_engine_job = self.mock_data_engine
        api.v1.jobs.account_tree = self.mock_account_tree
        token = json.loads(self.app.get('v1/system/token').data)['token']
        self.headers = {'Authorization': f'Bearer {token}'}

    # Test System Routes
    def test_system_health(self):
        '''Test GET method on the /v1/system/health endpoint returns 200'''
        response = self.app.get('v1/system/health')
        self.assertEqual(response.status_code, 200)

    def test_system_metrics(self):
        '''Test GET method on the /v1/system/metrics endpoint returns 200'''
        response = self.app.get('/v1/system/metrics')
        self.assertEqual(response.status_code, 200)

    # Test Jobs Routes
    def test_jobs_peek(self):
        '''Test GET method on /v1/jobs/'''
        self.mock_job_queue.peek.return_value = test_job
        response = self.app.get('/v1/jobs/', headers=self.headers)

        self.mock_job_queue.peek.assert_called()
        self.assertEqual(response.status_code, 200)

        job = json.loads(response.data)
        self.assertEqual(job["id"], test_job.id)
        self.assertEqual(job["priority"], test_job.priority)
        self.assertEqual(job["state"], test_job.state)

    def test_job_refresh(self):
        '''Test PUT method on /v1/jobs/'''
        response = self.app.put('/v1/jobs/', headers=self.headers)

        self.mock_job_queue.refresh.assert_called()
        self.assertEqual(response.status_code, 200)

    def test_job_pop(self):
        '''Test DELETE method on /v1/jobs/'''
        self.mock_job_queue.pop.return_value = test_job
        response = self.app.delete('/v1/jobs/', headers=self.headers)

        self.mock_job_queue.pop.assert_called()
        self.assertEqual(response.status_code, 200)

        job = json.loads(response.data)
        self.assertEqual(job["id"], test_job.id)
        self.assertEqual(job["priority"], test_job.priority)
        self.assertEqual(job["state"], test_job.state)

    # Test Job Items Routes
    def test_get_job_item(self):
        '''Test GET method on /v1/jobs/1'''
        self.mock_data_engine.query.get.return_value = test_job
        response = self.app.get('/v1/jobs/1', headers=self.headers)

        self.mock_data_engine.query.get.assert_called_with(1)
        self.assertEqual(response.status_code, 200)

        job = json.loads(response.data)
        self.assertEqual(job["id"], test_job.id)
        self.assertEqual(job["priority"], test_job.priority)
        self.assertEqual(job["state"], test_job.state)

    def test_delete_job_item(self):
        '''Test DELETE method on /v1/jobs/1'''
        self.mock_data_engine.query.get.return_value = test_job
        response = self.app.delete('/v1/jobs/1', headers=self.headers)

        self.assertEqual(response.status_code, 204)
        self.mock_data_engine.query.get.assert_called_with(1)
        self.mock_job_queue.remove.assert_called_with(test_job)

    def test_set_priority_job(self):
        '''Test GET method on /1/priority/1'''
        self.mock_data_engine.query.get.return_value = test_job
        response = self.app.put('/v1/jobs/1/priority/1', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        expected = test_job
        expected.priority = 1
        self.mock_job_queue.set.assert_called_with(expected)

    # Tree Route
    def test_source_tree(self):
        '''Test GET method on /1/source_tree'''
        self.mock_account_tree.data = {
            "account_id": 1,
            "dag": []
        }
        self.mock_account_tree.return_value = self.mock_account_tree
        response = self.app.get('/v1/jobs/1/source_tree', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.mock_account_tree.assert_called_with(1)
        self.mock_account_tree.refresh.assert_called()
