import logging

from flask import request
from flask_restplus import Resource
from lutron.api.manager.dbmethods import create_zonetype, update_zonetype, delete_zonetype
from lutron.api.manager.serializers import zone, zonetype, zonetype_with_zones
from lutron.api.restplus import api
from lutron.database.models import Zone, Zonetype

log = logging.getLogger(__name__)

ns = api.namespace('zonetypes', description='Zone types')

@ns.route('/')
class ZoneTypeCollection(Resource):

    @api.marshal_list_with(zonetype)
    def get(self):
        """
        Return details on the supported zone types.
        """
        zonetypes = Zonetype.query.all()
        return zonetypes