import os
import json
import serial
import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zone, update_zone, delete_zone
from lutron.api.manager.serializers import zone, zonetype, zonetype_with_zones
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

ns = api.namespace('zones', description='Operations related to RadioRA zones')

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

def getZMPStates():
    ser.reset_input_buffer()
    ser.write(str.encode("ZMPI\r\n"))

    # FIXME: this fails if cannot get a response, an error status should be returned instead of failing
    zoneStates = ser.readline().decode('utf-8').replace("\r","|")
    zoneStates = zoneStates.upper().lstrip('ZMP')
    
    return zoneStates

def addZoneStates(zones, stateZMP):
    
    if type(zones) is list:
        for index, item in enumerate(zones):
            if stateZMP[item.zone] == '0':
                zones[index].state= 'off'
            elif stateZMP[item.zone] == '1':
                zones[index].state = 'on'
            else:
                zones[index].state = 'Unknown'
    else:
        if stateZMP[zones.zone] == '0':
            zones.state = 'off'
        elif stateZMP[zones.zone] == '1':
            zones.state = 'on'
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

    # should creating zones exist?  There are a fixed number of Zones for RA-RS232 and Chronos devices (per system)
    @api.response(201, 'Zone successfully created.')
    @api.expect(zone)
    def post(self):
        """
        Creates a new zone.
        """
        data = request.json
        create_zone(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Zone not found.')
class ZoneItem(Resource):

    @api.marshal_with(zone)
    def get(self, id):
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

    @api.response(204, 'Zone successfully deleted.')
    def delete(self, id):
        """
        Deletes a zone.
        """
        delete_zone(id)
        return None, 204