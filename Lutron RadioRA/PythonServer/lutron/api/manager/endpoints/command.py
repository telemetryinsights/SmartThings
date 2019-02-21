import os
import time
import serial
import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zonetype, delete_zonetype, update_zonetype
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

ns = api.namespace('command', description='Operations related to lutron commands')

tty_path = os.environ['SERIAL_TTY'] if 'SERIAL_TTY' in os.environ else '/dev/ttyUSB0'

ser = serial.Serial(tty_path,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    dsrdtr=True,
                    rtscts=True,
                    timeout=2
                    )

@ns.route('/')
class ZMPI(Resource):
    def get(self):
        ser.reset_input_buffer()
        ser.write(str.encode("ZMPI\r\n"))
        
        receiveData = ser.readline().decode('utf-8').replace("\r","|")

        return {'lutron': receiveData}
    
@ns.route('/<cmd>')
class ApiLutronCmd(Resource):
    def get(self, cmd):
        
        ser.reset_input_buffer()
        ser.write(str.encode(cmd + "\r\n")) 
                
        receiveData = ser.readline().decode('utf-8').replace("\r","|")

        return {'lutron': receiveData}

@ns.route('/<cmd>/zone/<zone>/level/<level>')
class ApiLutronMultiCmd(Resource):
    def get(self, cmd, zone, level):
        ser.reset_input_buffer()
        ser.write(str.encode(cmd + "," + zone + "," + level + "\r\n"))

        receiveData = ser.readline().decode('utf-8').replace("\r","|")

        return {'lutron': receiveData}