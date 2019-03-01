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

raSerial = None

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    # inject RadioRA serial connection into the flask app
    flask_app.raSerial = raSerial 

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(manager_zones_namespace)
    api.add_namespace(manager_zonetypes_namespace)
    api.add_namespace(manager_command_namespace)
    flask_app.register_blueprint(blueprint)

    configure_app(flask_app)
    db.init_app(flask_app)

def main():

    raSerial = RadioRASerial(None)
    if raSerial is None:
        exit

    # default the RS232 device to a known state on startup
    raSerial.writeCommand('SFL,17,OFF') # force flashing mode off

    initialize_app(app)

    log.info('>>>>> Starting RadioRA Classic Smart Bridge v1.2 at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
