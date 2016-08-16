import sys
import os

sys.path.insert(0, "..\\")

import Database



4234
class DatabaseMock:
    def writeValue(self, value, time=None):
        time_string = 'default time' if time is None else time
        print(time_string, "value written: ", value)

    def getValues(self, start, stop):
        step = (stop - start) / 10
        return [(start + step * i, i) for i in range(10)]


# db = DatabaseMock()


db = Database.Database('192.168.1.26')
