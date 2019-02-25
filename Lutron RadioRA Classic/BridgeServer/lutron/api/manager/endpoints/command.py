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

ns = api.namespace('command', description='Raw RadioRA Classic command operations (*DEPRECATED*)')

# FIXME: share all the serial code in a separate file with command.py
tty_path = os.environ['SERIAL_TTY'] if 'SERIAL_TTY' in os.environ else '/dev/ttyUSB0'
tty_timeout = int(os.environ['SERIAL_TTY_TIMEOUT']) if 'SERIAL_TTY_TIMEOUT' in os.environ else 1

ser = serial.Serial(tty_path,
                    baudrate=9600, # 9600 baud is required by RA-RS232
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    dsrdtr=True,
                    rtscts=True,
                    timeout=tty_timeout
                    )

def _readline(ser_io):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser_io.read(1)
        if c:
            if c == eol:
                line += '|'
                break
            line += c
        else:
            break
    return bytes(line)

def writeSerialCommand(command):
    print(">>>>> Serial write: {}".format(command))
    ser.reset_input_buffer()
    ser.write((command + "\r\n").encode('utf-8'))

# NOTE: we should probably have a separate thread reading the asynchronous serial messages
#       since there are state updates that a write/read model won't catch
def readSerialData():
    start = time.time()
    result = _readline(ser)
    while ser.in_waiting:
        result = result + _readline(ser)
    result = result.decode('utf-8')
    end = time.time()

    print(">>>>> Serial read ({1:.0f} ms): {0}".format(result, 1000 * (end-start)))
    return result

####

@ns.route('/')
class ZMPI(Resource):
    def get(self):
        writeSerialCommand("ZMPI")
        return {'lutron': readSerialData()}
    
@ns.route('/<cmd>')
class ApiLutronCmd(Resource):
    def get(self, cmd):
        writeSerialCommand(cmd)
        return {'lutron': readSerialData()}

@ns.route('/<cmd>/zone/<zone>/level/<level>')
class ApiLutronMultiCmd(Resource):
    def get(self, cmd, zone, level):
        writeSerialCommand(cmd + "," + zone + "," + level)
        return {'lutron': readSerialData()}

@ns.route('/<cmd>/zone/<zone>/level/<level>')
class ApiLutronMultiCmd(Resource):
    def get(self, cmd, zone, level):
        writeSerialCommand(cmd + "," + zone + "," + level)
        return {'lutron': readSerialData()}
