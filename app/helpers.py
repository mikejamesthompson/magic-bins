import os
import csv, codecs, cStringIO
from datetime import datetime, time, timedelta

# Date manipulation helpers

def day_suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def next_collection(date, reference_date, frequency=7):
    delta = date - reference_date
    offset = timedelta(days=(frequency - (delta.days % frequency)))
    next = date + offset
    return next.strftime("%A, %e{S} %B %Y").replace('{S}', day_suffix(next.day))       


# CSV / unicode helpers

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self