from datetime import datetime
from lutron.database import db

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    zone = db.Column(db.IntegerText)

    zonetype_id = db.Column(db.Integer, db.ForeignKey('zonetype.id'))
    zonetype = db.relationship('Zonetype', backref=db.backref('zones', lazy='dynamic'))

    def __init__(self, name, zone, zonetype):
        self.name = name
        self.zone = zone
        self.zonetype = zonetype

    def __repr__(self):
        return '<Zone %r>' % self.name

class Zonetype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Zonetype %r>' % self.name