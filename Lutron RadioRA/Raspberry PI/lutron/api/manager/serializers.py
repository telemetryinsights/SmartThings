from flask_restplus import fields
from lutron.api.restplus import api

zone_details = api.model('Zone Details', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a zone'),
    'name': fields.String(required=True, description='Zone Name'),
    'zone': fields.Integer(required=True, description='Zone Number'),
    'zonetype_id': fields.Integer(attribute='zonetype.id'),
    'zonetype': fields.String(attribute='zonetype.name'),
})
