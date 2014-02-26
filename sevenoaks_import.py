import app
from app import db, models, helpers
from app.models import Collection, location_collections
from webhelpers.text import urlify

from datetime import datetime
import hashlib
import sys

class SevenoaksImporter:

    def __init__(self, filename):
        self.source = filename

    types = { 2 : "Household Waste", 3 : "Recycling", 4 : "Garden Waste"}

    collections = [{
        "name" : "Household Waste",
        "type" : "Household Waste", 
        "frequency" : 7,
        "reference_dates" : {
            'Monday' : datetime(2014,02,10),
            'Tuesday' : datetime(2014,02,11),
            'Wednesday' : datetime(2014,02,12),
            'Thursday' : datetime(2014,02,13),
            'Friday' : datetime(2014,02,14),
            'Saturday' : datetime(2014,02,15),
            'Sunday' : datetime(2014,02,16)}
        },
        {
        "name" : "Recycling",
        "type" : "Recycling", 
        "frequency" : 7,
        "reference_dates" : {
            'Monday' : datetime(2014,02,10),
            'Tuesday' : datetime(2014,02,11),
            'Wednesday' : datetime(2014,02,12),
            'Thursday' : datetime(2014,02,13),
            'Friday' : datetime(2014,02,14),
            'Saturday' : datetime(2014,02,15),
            'Sunday' : datetime(2014,02,16)}
        },
        {
        "name" : "Garden Waste 1",
        "type" : "Garden Waste",
        "frequency" : 14,
        "reference_dates" : {
            'Monday' : datetime(2014,02,03),
            'Tuesday' : datetime(2014,02,04),
            'Wednesday' : datetime(2014,02,05),
            'Thursday' : datetime(2014,02,06),
            'Friday' : datetime(2014,02,07),
            'Saturday' : datetime(2014,02,8),
            'Sunday' : datetime(2014,02,9)}
        },
        {
        "name" : "Garden Waste 2",
        "type" : "Garden Waste",
        "frequency" : "14",
        "reference_dates" : {
            'Monday' : datetime(2014,02,10),
            'Tuesday' : datetime(2014,02,11),
            'Wednesday' : datetime(2014,02,12),
            'Thursday' : datetime(2014,02,13),
            'Friday' : datetime(2014,02,14),
            'Saturday' : datetime(2014,02,15),
            'Sunday' : datetime(2014,02,16)}
        }]


    def importLocations(self):
        file = open(self.source)
        reader = helpers.UnicodeReader(file)
        
        for row in reader:
            location = models.Location(
                name = row[0],
                area = row[1],
                url_name = urlify(row[0]+" "+row[1])
                )
            db.session.add(location)
            db.session.commit()

            week = row[5]

            for column, t in self.types.items():
                # Skip columns with no collection
                if(row[column]=="None"):
                    continue
                # Change name for a garden waste collection based on week
                if(t == "Garden Waste"):
                    name = t + " "+week
                else:
                    name = t
                
                # Find stored collection that matches the one in the data source
                collection = Collection.query.filter_by(
                    type=t,
                    reference_date=self.getReferenceDate(name, row[column]),
                    frequency=self.getFrequency(name, row[column])
                    ).first()

                # And add it to the object
                location.collections.append(collection)

            db.session.commit()
        
        file.close()
        
        return True


    def createCollections(self):

        for c in self.collections:

            dates = c["reference_dates"]

            for day, date in dates.items():

                collection = models.Collection(
                    type = c["type"],
                    reference_date = date,
                    frequency = c["frequency"],
                    source_date = datetime(2014,02,20),
                    is_valid = True,
                    )
                db.session.add(collection)

        db.session.commit()

        return True


    def getReferenceDate(self, name, day):
        for c in self.collections:
            if c["name"]==name:
                return c["reference_dates"][day]
            else:
                continue


    def getFrequency(self, name, day):
        for c in self.collections:
            if c["name"]==name:
                return c["frequency"]
            else:
                continue


if __name__ == "__main__":
    importer = SevenoaksImporter('tmp/sevenoaks.csv')
    importer.createCollections()
    importer.importLocations()
