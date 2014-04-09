from app import db, helpers
from datetime import datetime, time, timedelta
from sqlalchemy import sql

location_collections = db.Table('location_collections',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)


class Collection(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type = db.Column(db.String(31), index = True)
    reference_date = db.Column(db.Date())
    frequency = db.Column(db.Integer())
    source_date = db.Column(db.DateTime())
    is_valid = db.Column(db.Boolean())

    def __repr__(self):
        return u'<Collection %r>' % (self.type + " every " + str(self.frequency) + " days, starting on: " + str(self.reference_date))

    def next_collection(self, date, reference_date, frequency=7):
        delta = date - reference_date
        offset = timedelta(days=(frequency - (delta.days % frequency)))
        next = date + offset

        schedule_change = ScheduleChange.query.filter(
                sql.expression.and_(
                    next >= ScheduleChange.date_from,
                    next <= ScheduleChange.date_to
                    )
                ).first()
        
        if(schedule_change):
            next_changed = next + timedelta(days=schedule_change.shift)
            return next.strftime("%A, %e{S} %B %Y").replace('{S}', helpers.day_suffix(next.day)), next_changed.strftime("%A, %e{S} %B %Y").replace('{S}', helpers.day_suffix(next_changed.day))
        else:
            return next.strftime("%A, %e{S} %B %Y").replace('{S}', helpers.day_suffix(next.day)), False


class Location(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), index = True)
    area = db.Column(db.String(255))
    url_name = db.Column(db.String(255), index = True, unique = True)
    collections = db.relationship('Collection', secondary = location_collections,
        backref = db.backref('locations', lazy ='dynamic'))

    def __repr__(self):
        return u'<Location %r>' % (self.name + ", " + self.area)


class ScheduleChange(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date_from = db.Column(db.Date(), index = True)
    date_to = db.Column(db.Date(), index = True)
    shift = db.Column(db.Integer())

    def __repr__(self):
        return u'<ScheduleChange %r>' % (str(self.shift) + " days, between " + str(self.date_from) + " and " + str(self.date_to))

