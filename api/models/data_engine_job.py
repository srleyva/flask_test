from api.databases import db, ma


class DataEngineJob(db.Model):
    """Wraps the data_engine_jobs table to expose id, state, priority, and
    created at. Also allows for sorting based on priority ascending and
    created at ascending. Equality checks are based on id.
    Attributes
    ----------
        id : int
            The id of the data engine job row.
        state : str
            The current job state.
        priority : int
            The job priority.
        created_at : DateTime
            When the job was created
    """

    __tablename__ = 'data_engine_jobs'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    priority = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id
        else:
            return False

    def __lt__(self, other):
        return self._comparator_() < other._comparator_()

    def __le__(self, other):
        return self._comparator_() <= other._comparator_()

    def __gt__(self, other):
        return self._comparator_() > other._comparator_()

    def __ge__(self, other):
        return self._comparator_() >= other._comparator_()

    def _comparator_(self):
        return (self.priority, self.created_at)

    def __repr__(self):
        return '<DataEngineJob {}, priority: {}, created_at: {}>'.format(
          self.id, self.priority, self.created_at
        )


class JobSchema(ma.ModelSchema):
    class Meta:
        model = DataEngineJob
