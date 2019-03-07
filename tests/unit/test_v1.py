"""Unit tests for the Jobs API v1 Service endpoint"""
import unittest
from unittest.mock import Mock

import api
from api.services.job_queue import JobQueue

mock_job_queue = Mock(JobQueue)
api.initialize_app(api.app, mock_job_queue)


class V1ServiceTest(unittest.TestCase):
    '''Tests for the Person endpoint'''
    def setUp(self):
        '''Set some state for each test in this class'''
        api.app.testing = True
        self.app = api.app.test_client()
        self.mock_job_queue = mock_job_queue

    def test_system_health(self):
        '''Test GET method on the /v1/system/health endpoint returns 200'''
        response = self.app.get('/v1/system/health')
        self.assertEqual(response.status_code, 200)

    def test_system_metrics(self):
        '''Test GET method on the /v1/system/metrics endpoint returns 200'''
        response = self.app.get('/v1/system/metrics')
        self.assertEqual(response.status_code, 200)

    def test_jobs_peek(self):
        '''Test GET method on /v1/jobs/'''
        self.mock_job_queue.peek.return_value = []
        response = self.app.get('/v1/jobs/')

        self.mock_job_queue.peek.assert_called()
        self.assertEqual(response.status_code, 200)

    def test_job_refresh(self):
        '''Test PUT method on /v1/jobs/'''
        response = self.app.put('/v1/jobs/')

        self.mock_job_queue.refresh.assert_called()
        self.assertEqual(response.status_code, 200)
