import logging
import traceback

from flask_restplus import Api
from flask_jwt_extended.exceptions import (
        NoAuthorizationError, InvalidHeaderError)
from sqlalchemy.orm.exc import NoResultFound

from api import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Data Engine Job',
          description='A demonstration of unit testing and integration')


@api.errorhandler
def default_error_handler(e):  # pragma: no cover
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):  # pragma: no cover
    log.warning(traceback.format_exc())
    return {'message': 'database result was required but none was found.'}, 404


@api.errorhandler(NoAuthorizationError)
@api.errorhandler(InvalidHeaderError)
def no_token_found(e):  # pragma: no cover
    return {'message': 'Bad Token'}, 400
