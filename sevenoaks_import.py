import app
from app import db, models, helpers
from app.models import Collection, location_collections
from webhelpers.text import urlify

from datetime import datetime, date
import hashlib
import sys

class SevenoaksImporter:

    def __init__(self, filename):
        self.source = filename

    # The value of the key here specifies the column number that the collection day 
    # is stored in in the CSV file (with numbering starting at 0)
    types = { 2 : "Household Waste", 3 : "Recycling", 4 : "Garden Waste"}

    # Dictionaries that define all possible collections in Sevenoaks DC with reference dates
    # representing when they have definitely happened in the past, used in calculating 
    # when the next collection is
    collections = [{
        "name" : "Household Waste",
        "type" : "Household Waste", 
        "frequency" : 7,
        "reference_dates" : {
            'Monday' : date(2014,02,10),
            'Tuesday' : date(2014,02,11),
            'Wednesday' : date(2014,02,12),
            'Thursday' : date(2014,02,13),
            'Friday' : date(2014,02,14),
            'Saturday' : date(2014,02,15),
            'Sunday' : date(2014,02,16)}
        },
        {
        "name" : "Recycling",
        "type" : "Recycling", 
        "frequency" : 7,
        "reference_dates" : {
            'Monday' : date(2014,02,10),
            'Tuesday' : date(2014,02,11),
            'Wednesday' : date(2014,02,12),
            'Thursday' : date(2014,02,13),
            'Friday' : date(2014,02,14),
            'Saturday' : date(2014,02,15),
            'Sunday' : date(2014,02,16)}
        },
        {
        "name" : "Garden Waste 1",
        "type" : "Garden Waste",
        "frequency" : 14,
        "reference_dates" : {
            'Monday' : date(2014,02,03),
            'Tuesday' : date(2014,02,04),
            'Wednesday' : date(2014,02,05),
            'Thursday' : date(2014,02,06),
            'Friday' : date(2014,02,07),
            'Saturday' : date(2014,02,8),
            'Sunday' : date(2014,02,9)}
        },
        {
        "name" : "Garden Waste 2",
        "type" : "Garden Waste",
        "frequency" : "14",
        "reference_dates" : {
            'Monday' : date(2014,02,10),
            'Tuesday' : date(2014,02,11),
            'Wednesday' : date(2014,02,12),
            'Thursday' : date(2014,02,13),
            'Friday' : date(2014,02,14),
            'Saturday' : date(2014,02,15),
            'Sunday' : date(2014,02,16)}
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
    
    change = app.models.ScheduleChange(date_from=date(2014,04,18),date_to=date(2014,04,25),shift=1)
    db.session.add(change)
    db.session.commit()
