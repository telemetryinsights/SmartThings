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

ns = api.namespace('zones', description='RadioRA Classic Zones')

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

def sendSerialCommand(command):
    print(">>>>> Serial write: {}".format(command))
    start = time.time()
    ser.reset_input_buffer()
    ser.write(str.encode(command + "\r\n"))
    end = time.time()
    print(">>>>> ... write took {0:.0f} ms)".format(1000 *(end-start)))

# NOTE: a SerialException is thrown if the read takes longer than the configured timeout
# NOTE: we should probably have a separate thread reading the asynchronous serial messages
#       since there are state updates that a write/read model won't catch
def receiveSerialResult():
    start = time.time()

    # FIXME: this is actually reading, but not completing and waiting for timeout!
    # big performance improvement can be had here
    
    result = ser.readline().decode('utf-8')
    end = time.time()
    print(">>>>> Serial reply: {0} (after {1:.0f} ms)".format(result, 1000 *(end-start)))
    return result

####

# ZMP response from either ZMPI request *OR* from response stream
#  ZMP,010000001000000000000000000000XX
def handleZMPResponse():
    # NOTE: returns X if not assigned!
    return

def getZMPStates():
    sendSerialCommand("ZMPI")
    zoneStates = receiveSerialResult().replace("\r","|")
    zoneStates = zoneStates.upper().lstrip('ZMP')
    return zoneStates

def addZoneStates(zones, stateZMP):
    log.info("Entered: addZoneStates()")

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
        elif stateZMP[item.zone] == 'X':
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
        zones = Zone.query.all()
        zones = addZoneStates(zones, getZMPStates())        
        return zones    

    # FIXME: should creating zones exist?  There are a fixed number of Zones for RA-RS232 and Chronos devices (per system)
#    @api.response(201, 'Zone successfully created.')
#    @api.expect(zone)
#    def post(self):
#        """
#        Creates a new zone.
#        """
#        data = request.json
#        create_zone(data)
#        return None, 201

#####

def sendAll(command, suffix):
    for zone in range(16):
        sendSerialCommand(command + "," + zone + "," + suffix)

# FIXME: test of more direct control of single zones...using ZSI command
@ns.route('/<int:id>/control')
@api.response(404, 'Zone not found.')
class ZoneItemControl(Resource):

    @api.marshal_with(zone)
    def get(self, id):
        try:
            sendAll("SDL", "100")

            sendSerialCommand("ZSI")
            zoneStates = receiveSerialResult().replace("\r","|")

            # FIXME: how is 404 triggered?  What if I send zone 77?

            log.info("Zone States: " + zoneStates)
            print("Zone States: " + zoneStates + "\n")

            iZone = addZoneStates(Zone.query.filter(Zone.id == id).one(), getZMPStates())
            return iZone

        except Exception as e:
            log.exception("Unexpected error")
            return None, 500  # 500 Internal Server Error

    @api.expect(zone)
    @api.response(204, 'Zone successfully updated.')
    def put(self, zone):
        """
        Sets the switch on or dimmer level

        Use this method to change attributes of a zone.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "zone": "Zone Number"
          "state": "on/off"
          "level": "Dimmer level (optional)"
        }
        ```

        * Specify the ID of the zone to control in the request URL path.
        """
        try:
            data = request.json
            print ">>>> received " + data + "\n"

            zoneIsDimmer = True

            dimmerLevel = 50
            state = OFF

            # NOTE: the SDL/SSL commands do not send a response
            if zoneIsDimmer == True:
                # if state = 'on' then dimmerLevel = 100 ???
                # SDL,<Zone Number>,<Dimmer Level>(,<Fade Time>){(,<System)}
                sendSerialCommand("SDL," + zone + "," + dimmerLevel)
            else:
                # SSL,<Zone Number>,<State>(,<Delay Time>){(,<System>)}
                sendSerialCommand("SSL," + zone + "," + state)
            # FIXME: SGS for Grafik Eye
            #
            # FIXME: we should probably return the same content as the SRI / requests
            return None, 204

        except Exception as e:
            print ">>>> WHAT\n"
            log.error("Unexpected error:" + e)
            return None, 500  # 500 Internal Server Error


####

@ns.route('/<int:id>')
@api.response(404, 'Zone not found.')
class ZoneItem(Resource):

    @api.marshal_with(zone)
    def get(self, id):
        # FUTURE: note that ZSI command might be faster/more efficient here than filter the states
        iZone = addZoneStates(Zone.query.filter(Zone.id == id).one(), getZMPStates())
        return iZone

    @api.expect(zone)
    @api.response(204, 'Zone successfully updated.')
    def put(self, id):
        """
        Updates a zone.

        Use this method to change attributes of a zone.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "Zone Name"
          "zone": "Zone Number"
          "system": "System Number"
          "zonetype_id": "Zone type ID"
        }
        ```

        * Specify the ID of the zone to modify in the request URL path.
        """
        data = request.json
        update_zone(id, data)
        return None, 204

#    @api.response(204, 'Zone successfully deleted.')
#    def delete(self, id):
#        """
#        Deletes a zone.
#        """
#        delete_zone(id)
#        return None, 204
