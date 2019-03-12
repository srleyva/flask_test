===================
Data Engine Job API
===================

* Not gevent need to be replaced as it increased the integration and build time by over 300%


|build| |coverage|

This Data Engine Job API Project
is a demonstration of a CICD Pipeline
for a Python Project.


Documentation
=============

See `requirements.txt <https://github.com/srleyva/data_engine_job_api/blob/master/requirements.txt>`_
file for additional dependencies:

* Python 3.7


Installation
------------

For a manual install:

Run
::

    pip install .

Configuration
-------------

This app was designed by the `12 Factor App Methodology <https://12factor.net/>`_.
As such configuration can be set in the Environment with plans to allow config files
and CLI Args.

The following options are currently available:

+----------------------+----------------------------+--------------------------------------------------------+
| Configuration Option |         Explanation        | Default Value                                          |
+======================+============================+========================================================+
|      API_DEBUG       | Verbosity in App Logs      |   False                                                |
+----------------------+----------------------------+--------------------------------------------------------+
|   API_DATABASE_URI   | Database connection string | postgres://postgres:@postgres:5432/circle_test'        |
+----------------------+----------------------------+--------------------------------------------------------+
|    JWT_SECRET_KEY    | Secret used to sign JWT    |       secret-key                                       |
+----------------------+----------------------------+--------------------------------------------------------+


Running Tests
-------------

Run tests by executing
::

    mkvirtualenv api
    pip install tox
    tox

.. |build| image:: https://circleci.com/gh/srleyva/data_engine_job_api.svg?style=svg&circle-token=96edeb740d9f323e8a8530f9f23e1134c50c8c9d
    :target: https://circleci.com/gh/srleyva/data_engine_job_api
.. |coverage| image:: https://img.shields.io/badge/Coverage-98%25-brightgreen.svg
    :target: https://circleci.com/gh/srleyva/data_engine_job_api
