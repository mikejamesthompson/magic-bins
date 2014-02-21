from app import db

location_collections = db.Table('location_collections',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)


class Collection(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type = db.Column(db.String(31), index = True)
    reference_date = db.Column(db.DateTime())
    frequency = db.Column(db.Integer())
    source_date = db.Column(db.DateTime())
    is_valid = db.Column(db.Boolean())

    def __repr__(self):
        return u'<Collection %r>' % (self.type + " every " + str(self.frequency) + " days, starting on: " + str(self.reference_date))


class Location(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), index = True)
    area = db.Column(db.String(255), index = True)
    collections = db.relationship('Collection', secondary=location_collections,
        backref=db.backref('locations', lazy='dynamic'))

    def __repr__(self):
        return '<Location %r>' % (self.name + ", " + self.area)