import os
import json
import logging

from flask import request
from flask_restplus import Resource

#import myapplication.myviews.view

from lutron.api.manager.dbmethods import create_zone, update_zone, delete_zone
from lutron.api.manager.serializers import zone, zonetype, zonetype_with_zones
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype
#from radiora-classic-bridge import raSerial

LOG = logging.getLogger(__name__)

UNKNOWN_STATE = 'Unknown'
STATE_ON = 'on'
STATE_OFF = 'off'

LUTRON = 'lutron'

# FIXME: what must be configured
#  - for each zone, what zone type of switch/dimmer it is (default to dimmer)
#  - we should allow client to specify if they want ALL the zones (e.g. including Unassigned)

ns = api.namespace('zones', description='Zone operations')

raSerial = None  # FIXME

# FIXME: this will not work on Lutron installations where a Chronos System Bridge or
# Timeclock is setup to be a System Bridge where TWO zone maps will be returned (a total of 64 zones)
def getAllZoneStates():
    api.raSerial.writeCommand('ZMPI')
    zoneStates = raSerial.readData().lstrip('ZMP')
    return zoneStates

def mergeZoneStates(zones, stateZMP):
    # NOTE: ZMP always returns state for all 32 zones, PLUS if it is a bridged system
    # it will return two sets, with ",S1" and ",S2" at the end of the result
    # this does not support bridged systems currently
    if type(zones) is list:
        for index, item in enumerate(zones):
            if stateZMP[item.zone] == '0':
                zones[index].state = STATE_OFF
            elif stateZMP[item.zone] == '1':
                zones[index].state = STATE_ON
            elif stateZMP[item.zone] == 'X':
                # force type to be Unassigned (since we know it isn't assigned to a dimmer or switch)
                zones[index].zonetypeid  = '0' # Unassigned
                zones[index].state = UNKNOWN_STATE
            else:
                zones[index].state = UNKNOWN_STATE
    else:
        if stateZMP[zones.zone] == '0':
            zones.state = STATE_OFF
        elif stateZMP[zones.zone] == '1':
            zones.state = STATE_ON
        elif stateZMP[zones.zone] == 'X':
            # force type to be Unassigned (since we know it isn't assigned to a dimmer or switch)
            zones.zonetypeid = '0' # Unassigned
            zones.state = UNKNOWN_STATE
        else:
            zones.state = UNKNOWN_STATE

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

@ns.route('/<int:id>/dim/<level>')
class ZoneDimmerLevel(Resource):
    def get(self, zone, level):
        # SDL,<Zone Number>,<Dimmer Level>(,<Fade Time>){(,<System)}
        raSerial.writeCommand("SDL," + zone + "," + level)
        return { LUTRON: raSerial.readData() }

@ns.route('/<int:id>/switch/on')
class ZoneSwitchOn(Resource):
    def get(self, zone):
        # SSL,<Zone Number>,<State>(,<Delay Time>){(,<System>)}
        raSerial.writeCommand("SSL," + zone + ",ON")
        return { LUTRON: raSerial.readData() }

@ns.route('/<int:id>/switch/off')
class ZoneSwitchOff(Resource):
    def get(self, zone):
        raSerial.writeCommand("SSL," + zone + ",OFF")
        return { LUTRON: raSerial.readData() }

@ns.route('/all/on')
class AllOn(Resource):
    def get(self):
        raSerial.writeCommand("BP,16,ON")
        return { LUTRON: raSerial.readData() }

@ns.route('/all/off')
class AllOff(Resource):
    def get(self):
        raSerial.writeCommand("BP,17,OFF")
        return { LUTRON: raSerial.readData() }

@ns.route('/all/flash/on')
class FlashOn(Resource):
    def get(self):
        raSerial.writeCommand("SFM,16,ON")
        return { LUTRON: raSerial.readData() }

@ns.route('/all/flash/off')
class FlashOff(Resource):
    def get(self):
        raSerial.writeCommand("SFM,17,OFF")
        return { LUTRON: raSerial.readData() }