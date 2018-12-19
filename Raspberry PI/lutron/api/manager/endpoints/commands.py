import os
import time
import serial
import logging

from flask import request
from flask_restplus import Resource
from lutron.api.blog.business import create_zonetype, delete_zonetype, update_zonetype
from lutron.api.restplus import api
from lutron.database.models import Category

log = logging.getLogger(__name__)

ns = api.namespace('commands', description='Operations related to lutron commands')

ser = serial.Serial('/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    xonxoff=True,
                    rtscts=True,
                    timeout=2
                    )

@ns.route('/')
class ZMPI(Resource):
    def get(self):
        ser.write(str.encode("ZMPI\r\n"))

        receiveData = ''
        while True:
            receiveByte = (ser.read())

            if receiveByte == b'\r':
                break
            receiveData = receiveData + receiveByte.decode('utf-8')
        return {'lutron': receiveData}
    
@ns.route('/command/<cmd>')
class ApiLutronCmd(Resource):
    def get(self, cmd):
        ser.write(str.encode(cmd + "\r\n"))

        receiveData = ''
        while True:
            receiveByte = (ser.read())

            if receiveByte == b'\r':
                break
            receiveData = receiveData + receiveByte.decode('utf-8')
        return {'lutron': receiveData}

@ns.route('/command/<cmd>/zone/<zone>/level/<level>')
class ApiLutronMultiCmd(Resource):
    def get(self, cmd, zone, level):
        ser.write(str.encode(cmd + "," + zone + "," + level + "\r\n"))

        receiveData = ''
        while True:
            receiveByte = (ser.read())

            if receiveByte == b'\r':
                break
            receiveData = receiveData + receiveByte.decode('utf-8')
        return {'lutron': receiveData}g
