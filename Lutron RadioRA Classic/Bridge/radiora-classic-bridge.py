import os
import time
import logging.config

from lutron import settings
from lutron.serial import RadioRASerial

from flask import Flask, Blueprint
from lutron.api.manager.endpoints.zones import ns as manager_zones_namespace
from lutron.api.manager.endpoints.zonetypes import ns as manager_zonetypes_namespace
from lutron.api.manager.endpoints.command import ns as manager_command_namespace
from lutron.api.restplus import api
from lutron.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(manager_zones_namespace)
    api.add_namespace(manager_zonetypes_namespace)
    api.add_namespace(manager_command_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

def main():

# tty = '/dev/ttyUSB0' if not os.environ['SERIAL_TTY'] else os.environ['SERIAL_TTY']

    print("testing...")
    raSerial = RadioRASerial(None)
    exit

    if not os.path.exists(tty):
        log.error(">>>>> Serial device '%s' does not exist: set SERIAL_TTY environment variable to your /dev/tty interface", tty)
        exit
    else:
        log.info('>>>>> Communicating with Lutron RadioRA Classic hardware module via serial %s', tty)

    # FIXME: set the RS232 device into a default space
    # sendSerialCommand("VERI") -> REV,M3.14,S1.01    print it out
    # sendSerialCommand("SFL,17,OFF") # force flashing mode off

    configure_app(flask_app)
    initialize_app(app)

    log.info('>>>>> Starting server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
