from lutron.database import db
from lutron.database.models import Zone, Zonetype

KEY_NAME = 'name'
KEY_ZONE = 'zone'
KEY_SYSTEM = 'system'

def create_zone(data):
    name = data.get('name')
    zone = data.get('zone')
    system = data.get('system')
    zonetypeid = data.get('zonetypeid')
    zoned = Zone(name, zone, system, zonetypeid)
    db.session.add(zoned)
    db.session.commit()

def update_zone(zoneid, data):
    zoned = Zone.query.filter(Zone.id == zoneid).one()
    zoned.name = data.get('name')
    zoned.zone = data.get('zone')
    zoned.system = data.get('system')
    zoned.zonetypeid = data.get('zonetypeid')
    db.session.add(zoned)
    db.session.commit()

def delete_zone(zone_id):
    zoned = Zone.query.filter(Zone.id == zoneid).one()
    db.session.delete(zoned)
    db.session.commit()

def create_zonetype(data):
    name = data.get('name')
    zonetypeid = data.get('id')

    zonetype = Zonetype(name)
    if zonetypeid:
        zonetype.id = zonetypeid

    db.session.add(zonetype)
    db.session.commit()

def update_zonetype(zonetypeid, data):
    zonetype= Zonetype.query.filter(Zonetype.id == zonetypeid).one()
    zonetype.name = data.get('name')
    db.session.add(zonetype)
    db.session.commit()

def delete_zonetype(zonetypeid):
    zonetype = Zonetype.query.filter(Zonetype.id == zonetypeid).one()
    db.session.delete(zonetype)
    db.session.commit()
