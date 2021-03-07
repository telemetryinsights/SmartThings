import os
import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zonetype, delete_zonetype, update_zonetype
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

# FIXME: we will deprecate the raw CMD interface for security reseasons (or at least
# require a config option to enable this for those who don't care)
ns = api.namespace('command', description='Raw RadioRA Classic command operations (*DEPRECATED*)')

raSerial = None

LUTRON = 'lutron'

@ns.route('/')
class ZMPI(Resource):
    def get(self):
        raSerial.writeCommand("ZMPI")
        return { LUTRON: raSerial.readData() }
    
@ns.route('/<cmd>')
class ApiLutronCmd(Resource):
    def get(self, cmd):
        raSerial.writeCommand(cmd)
        return { LUTRON: raSerial.readData() }

@ns.route('/<cmd>/zone/<zone>/level/<level>')
class ApiLutronMultiCmd(Resource):
    def get(self, cmd, zone, level):
        raSerial.writeCommand(cmd + "," + zone + "," + level)
        return { LUTRON: raSerial.readData() }
