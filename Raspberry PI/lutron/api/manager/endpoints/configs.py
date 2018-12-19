import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zone, update_zone, delete_zone
from lutron.api.manager.serializers import zone_details
from lutron.api.manager.parsers import pagination_arguments
from lutron.api.restplus import api
from lutron.database.models import zone

log = logging.getLogger(__name__)

ns = api.namespace('configs', description='Operations related to lutron configs')

@ns.route('/')
class Configs(Resource):
    def get(self):
        ser.write(str.encode("ZMPI\r\n"))

        receiveData = ''
        while True:
            receiveByte = (ser.read())

            if receiveByte == b'\r':
                break
            receiveData = receiveData + receiveByte.decode('utf-8')
        return {'lutron': receiveData}