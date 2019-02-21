import logging
import traceback

from flask_restplus import Api
from lutron import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(title='Lutron RadioRA Classic Gateway', version='1.0', 
          description='Exposes RESTful APIs for interacting with Lutron RadioRA Classic switches/dimmers')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
