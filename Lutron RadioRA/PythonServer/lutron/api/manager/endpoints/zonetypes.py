import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zonetype, update_zonetype, delete_zonetype
from lutron.api.manager.serializers import zone, zonetype, zonetype_with_zones
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

ns = api.namespace('zonetypes', description='Operations related to lutron zonetypes')

@ns.route('/')
class ZoneTypeCollection(Resource):

    @api.marshal_list_with(zonetype)
    def get(self):
        """
        Returns list of zone types.
        """
        zonetypes = Zonetype.query.all()
        return zonetypes

    @api.response(201, 'Zone Type successfully created.')
    @api.expect(zonetype)
    def post(self):
        """
        Creates a new zone type.
        """
        data = request.json
        create_zonetype(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Zone type not found.')
class ZonetypeItem(Resource):

    @api.marshal_with(zonetype_with_zones)
    def get(self, id):
        """
        Returns a zone type with a list of associated zones.
        """
        return Zonetype.query.filter(Zonetype.id == id).one()

    @api.expect(zonetype)
    @api.response(204, 'Zone type successfully updated.')
    def put(self, id):
        """
        Updates a zone type.

        Use this method to change the name of a zone type.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "New Zone Type Name"
        }
        ```

        * Specify the ID of the zone type to modify in the request URL path.
        """
        data = request.json
        update_zonetype(id, data)
        return None, 204

    @api.response(204, 'Zone Type successfully deleted.')
    def delete(self, id):
        """
        Deletes zone Type.
        """
        delete_zonetype(id)
        return None, 204