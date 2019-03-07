from api.models.data_engine_job import DataEngineJob
import threading


class __Singleton(type):
    """Utility for making the JobQueue service a singleton."""

    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance


class JobQueue(metaclass=__Singleton):
    """Provides refresh, next, set, and remove methods for building and retreiving
    the next job out of the queue as well as adding/updating and removing them.
    This class is a singleton and must be accessed through the class instance()
    method.
    """

    QUEUED_JOBS_FILTER = DataEngineJob.state.in_([
        'new', 'retryable_failure', 'delayed_start'
    ])

    def __init__(self):
        self.lock = threading.Lock()
        self.jobs = []
        self.refresh()

    def set(self, job):
        """Adds or updates the priority of a job in the queue.
        Parameters:
            job (DataEngineJob): The job to add/update.
        """

        self.lock.acquire()
        try:
            if job in self.jobs:
                self.jobs.remove(job)

            self.jobs.append(job)
            self.jobs.sort()
        finally:
            self.lock.release()

    def pop(self):
        """Returns the next job in the queue and removes it or None.
        Returns:
            job (JobEngine): The next job.
        """

        self.lock.acquire()
        try:
            if len(self.jobs) > 0:
                return self.jobs.pop(0)
        finally:
            self.lock.release()

    def peek(self):
        """Returns the next job in the queue but does not remove it.
        Returns:
            job (JobEngine): The next job.
        """

        if len(self.jobs) > 0:
            return self.jobs[0]

    def remove(self, job):
        """Removes the provided job if it is in the queue.
        Parameters:
            job (DataEngineJob): The job to remove.
        """

        self.lock.acquire()
        try:
            self.jobs.remove(job)
        except ValueError:
            pass
        finally:
            self.lock.release()

    def refresh(self):
        """Refreshes the contents of the queue by loading all queued jobs from
        the database.
        """
        self.lock.acquire()
        try:
            self.jobs.clear()
            result = DataEngineJob.query.filter(self.QUEUED_JOBS_FILTER).all()
            for job in result:
                self.jobs.append(job)

            self.jobs.sort()
        finally:
            self.lock.release()
