import copy
from datetime import datetime
import unittest
from unittest.mock import Mock

from api.services.job_queue import JobQueue
from api.services.source_tree import AccountSourceTree

from api.models.data_engine_job import DataEngineJob
from api.databases import db


class JobQueueServiceTest(unittest.TestCase):
    '''Tests for the V1 endpoints'''
    def setUp(self):
        '''Set some state for each test in this class'''
        self.mock_data_engine = Mock(DataEngineJob)
        self.test_jobs = []
        for i in range(3):
            self.test_jobs.append(_create_test_jobs(i+1, (i+1)*10))
        self.test_jobs.sort()
        self.mock_data_engine.query.filter().all.return_value = self.test_jobs
        self.job_queue = JobQueue(self.mock_data_engine)
        self.jobs = self.job_queue.jobs

    def tearDown(self):
        self.test_jobs = []

    def test_job_queue_init(self):
        '''test the setting of jobs and refresh call'''
        self.assertEqual(self.jobs, self.test_jobs)
        self.mock_data_engine.query.filter(
            self.job_queue.QUEUED_JOBS_FILTER
        ).all.assert_called()

    def test_job_queue_pop(self):
        '''test the pop of job queue'''
        job = self.job_queue.pop()
        self.assertEqual(job, self.test_jobs[0])

    def test_job_queue_peek(self):
        '''test the peek of job queue'''
        job = self.job_queue.peek()
        self.assertEqual(job, self.test_jobs[0])

    def test_job_queue_set(self):
        '''test the set of job queue'''
        new_job = copy.copy(self.test_jobs[0])
        new_job.priority = 200
        self.job_queue.set(new_job)
        self.assertEqual(new_job, self.test_jobs[0])

    def test_job_remove(self):
        '''test the set of job queue'''
        job = copy.copy(self.test_jobs[0])
        self.job_queue.remove(job)
        self.assertNotIn(job, self.jobs)


def _create_test_jobs(id, priority, created_at=datetime.now(), state="new"):
    test_job = DataEngineJob()
    test_job.id = id
    test_job.created_at = created_at
    test_job.state = state
    test_job.priority = priority
    return test_job


class AccountTreeServiceTest(unittest.TestCase):
    '''Tests for the V1 endpoints'''
    def setUp(self):
        '''Set some state for each test in this class'''
        self.mock_db = Mock(db)
        self.source_tree = AccountSourceTree(1, database=self.mock_db)

    def test_account_tree_init(self):
        data = {
            "account_id": 1,
            "dag": []
        }
        self.assertEqual(data, self.source_tree.data)
        self.assertEqual(1, self.source_tree.account_id)

    def test_refresh(self):
        test_return = [
            {
                "parent_id": 1,
                "report_id": 123
            },
            {
                "parent_id": 1,
                "report_id": 122
            }
        ]
        self.mock_db.engine.execute.return_value = test_return
        self.source_tree.refresh()
        self.mock_db.engine.execute.assert_called_with(
            self.source_tree.SOURCE_TREE_SQL.format(account_id=1))
        # TODO Get with john to test response
        # self.assertIn(
        #     test_return,
        #     self.source_tree.data["dag"])
