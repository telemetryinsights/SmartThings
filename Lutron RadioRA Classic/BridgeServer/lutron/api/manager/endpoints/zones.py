import os
import json
import time
import serial
import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zone, update_zone, delete_zone
from lutron.api.manager.serializers import zone, zonetype, zonetype_with_zones
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

# FIXME: what must be configured
#  - which /dev/tty device to use
#  - for each zone, what zone type of switch/dimmer it is (default to dimmer)
#  - we should allow client to specify if they want ALL the zones (e.g. including Unassigned)

ns = api.namespace('zones', description='Zone operations')

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

# not the most efficient reading one byte at a time, but it is way faster than
# waiting for a 1 or 2 second timeout on every read. This should be fixed in
# the future.
def readSerialData():
    start = time.time()
    result = result = _readline(ser)
    while ser.in_waiting:
        result = result + _readline(ser)
    result = result.decode('utf-8').upper()
    end = time.time()

    print(">>>>> Serial read ({1:.0f} ms): {0}".format(result, 1000 * (end-start)))
    return result

####

# FIXME: this will not work on Lutron installations where a Chronos System Bridge or
# Timeclock is setup to be a System Bridge where TWO zone maps will be returned (a total of 64 zones)
def getAllZoneStates():
    writeSerialCommand("ZMPI")
    zoneStates = readSerialData().lstrip('ZMP')
    return zoneStates

def mergeZoneStates(zones, stateZMP):
    # NOTE: ZMP always returns state for all 32 zones, PLUS if it is a bridged system
    # it will return two sets, with ",S1" and ",S2" at the end of the result
    # this does not support bridged systems currently
    if type(zones) is list:
        for index, item in enumerate(zones):
            if stateZMP[item.zone] == '0':
                zones[index].state = 'off'
            elif stateZMP[item.zone] == '1':
                zones[index].state = 'on'
            elif stateZMP[item.zone] == 'X':
                # force type to be Unassigned (since we know it isn't assigned to a dimmer or switch)
                zones[index].zonetypeid  = '0' # Unassigned
                zones[index].state = 'Unknown'
            else:
                zones[index].state = 'Unknown'
    else:
        if stateZMP[zones.zone] == '0':
            zones.state = 'off'
        elif stateZMP[zones.zone] == '1':
            zones.state = 'on'
        elif stateZMP[zones.zone] == 'X':
            # force type to be Unassigned (since we know it isn't assigned to a dimmer or switch)
            zones.zonetypeid = '0' # Unassigned
            zones.state = 'Unknown'
        else:
            zones.state = 'Unknown'

    return zones   

@ns.route('/')
class ZoneCollection(Resource):
    
    @api.marshal_list_with(zone)
    def get(self):
        # read zone configuration from DB
        zones = Zone.query.all()
        # merge current states for each zone from hardware module
        zones = mergeZoneStates(zones, getAllZoneStates())        
        return zones

####

@ns.route('/<int:id>')
@api.response(404, 'Zone not found')
class ZoneItem(Resource):

    @api.marshal_with(zone)
    def get(self, id):
        return mergeZoneStates(Zone.query.filter(Zone.id == id).one(), getAllZoneStates())

    @api.expect(zone)
    @api.response(204, 'Zone successfully updated')
    def put(self, id):
        """
        Update attributes for a zone

        Send a JSON object with the new name in the request body with the ID of the zone to modify in the request URL path.

        ```
        {
          "name": "Zone name"
          "zonetypeid": "Zone type identifier [0, 1, 2, or 3]"
          "default_level": "Default level for dimmer (not yet supported)"
        }
        ```
        """
        data = request.json
        update_zone(id, data)
        return None, 204

# FIXME: I'm not sure we want REST Get with side effect, but it is very convenient!
@ns.route('/<int:id>/dim/<level>')
class ZoneDimmerLevel(Resource):
    def get(self, zone, level):
        # SDL,<Zone Number>,<Dimmer Level>(,<Fade Time>){(,<System)}
        writeSerialCommand("SDL," + zone + "," + level)
        return {'lutron': readSerialData()}

@ns.route('/<int:id>/switch/on')
class ZoneSwitchOn(Resource):
    def get(self, zone):
        # SSL,<Zone Number>,<State>(,<Delay Time>){(,<System>)}
        writeSerialCommand("SSL," + zone + ",ON")
        return {'lutron': readSerialData()}

@ns.route('/<int:id>/switch/off')
class ZoneSwitchOff(Resource):
    def get(self, zone):
        writeSerialCommand("SSL," + zone + ",OFF")
        return {'lutron': readSerialData()}

@ns.route('/all/on')
class AllOn(Resource):
    def get(self):
        writeSerialCommand("BP,16,ON")
        return {'lutron': readSerialData()}

@ns.route('/all/off')
class AllOff(Resource):
    def get(self):
        writeSerialCommand("BP,17,OFF")
        return {'lutron': readSerialData()}

@ns.route('/all/flash/on')
class FlashOn(Resource):
    def get(self):
        writeSerialCommand("SFM,16,ON")
        return {'lutron': readSerialData()}

@ns.route('/all/flash/off')
class FlashOff(Resource):
    def get(self):
        writeSerialCommand("SFM,17,OFF")
        return {'lutron': readSerialData()}