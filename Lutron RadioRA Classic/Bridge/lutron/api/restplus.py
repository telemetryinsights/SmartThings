import logging
import traceback

from lutron import settings
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

APP_NAME='Lutron RadioRA Classic Smart Bridge'

api = Api(title=APP_NAME, version='1.0.1', 
          description='RESTful APIs for controlling a Lutron RadioRA Classic lighting system through a serial connection')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required, but none found.'}, 404
