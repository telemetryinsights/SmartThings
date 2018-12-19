from lutron.database import db
from lutron.database.models import Zone, Zonetype

def create_zone(data):
    name = data.get('name')
    zone = data.get('zone')
    zonetype_id = data.get('zonetype_id')
    zonetype = Zonetype.query.filter(Zonetype.id == zonetype_id).one()
    zone = Zone(name, zone, zonetype)
    db.session.add(zone)
    db.session.commit()

def update_zone(zone_id, data):
    zone = Post.query.filter(Zone.id == zone_id).one()
    zone.name = data.get('name')
    zone.zone = data.get('zone')
    zonetype_id = data.get('zonetype_id')
    zone.zonetype = Zonetype.query.filter(Zonetype.id == zonetype_id).one()
    db.session.add(zone)
    db.session.commit()

def delete_zone(zone_id):
    zone = Zone.query.filter(Zone.id == zone_id).one()
    db.session.delete(zone)
    db.session.commit()

def create_zonetype(data):
    name = data.get('name')
    zonetype_id = data.get('id')

    zonetype = Zonetype(name)
    if zonetype_id:
        zonetype.id = zonetype_id

    db.session.add(zonetype)
    db.session.commit()

def update_zonetype(zonetype_id, data):
    zonetype= Zonetype.query.filter(Zonetype.id == zonetype_id).one()
    zonetype.name = data.get('name')
    db.session.add(zonetype)
    db.session.commit()

def delete_zonetype(zonetype_id):
    zonetype = Zonetype.query.filter(Zonetype.id == zonetype_id).one()
    db.session.delete(zonetype)
    db.session.commit()
