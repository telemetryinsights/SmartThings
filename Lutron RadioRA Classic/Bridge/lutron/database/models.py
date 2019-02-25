from datetime import datetime
from lutron.database import db

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # FIXME: do we really need to store a name for each zone (vs just refering to them by 'zone-1', etc)
    zone = db.Column(db.Integer)
    system = db.Column(db.Integer) # NOTE: multiple systems not supported right now (since each system would have a separate serial port)
    state = db.Column(db.String(10)) # FIXME: should we really store the "last state"? Or just keep this in memory...minimize writes to SD cards/SSDs
    zonetypeid = db.Column(db.Integer, db.ForeignKey('zonetype.id'))
    zonetype = db.relationship('Zonetype', backref=db.backref('zones', lazy='dynamic'))

    def __init__(self, name, zone, system, zonetypeid):
        self.name = name
        self.zone = zone
        self.system = system
        self.state = state
        self.zonetypeid = zonetypeid

    def __repr__(self):
        return '<Zone %r>' % self.name

class Zonetype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Zonetype %r>' % self.name