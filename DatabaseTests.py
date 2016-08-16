import unittest
import datetime
from Database import Database
from configparser import ConfigParser


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.configparser = ConfigParser()
        self.configparser.read("config.ini")
        self.adminCredentials = dict(adminUser=self.__getConfigValue('adminUser'),
                                     adminPassword=self.__getConfigValue('adminPassword'))
        self.databaseName = self.__getConfigValue("database")
        self.host = self.__getConfigValue('host')

    def test_dropping_creating(self):
        db = self.__createTarget()
        if db.checkDatabaseExist(**self.adminCredentials):
            print("database exist ")
            db.drop(**self.adminCredentials)
        self.assertFalse(db.checkDatabaseExist(**self.adminCredentials))
        db.create(**self.adminCredentials)
        self.assertTrue(db.checkDatabaseExist(**self.adminCredentials))
        db.drop(**self.adminCredentials)
        self.assertFalse(db.checkDatabaseExist(**self.adminCredentials))

    def test_writing_reading_values(self):
        db = self.__createTarget()
        if not db.checkDatabaseExist(**self.adminCredentials):
            print("creating database")
            db.create(**self.adminCredentials)
        now = datetime.datetime.now()
        for i in range(-5, 5):
            db.writeValue(42 + i, now + datetime.timedelta(seconds=i))

        values = db.getValues(now - datetime.timedelta(seconds=1),
                              now + datetime.timedelta(seconds=1))
        self.assertEqual(len(values), 3)

        for i in range(3):
            self.assertEqual(values[i][1], 41 + i)

    def __getConfigValue(self, settingName):
        """

        :type settingName: str
        :rtype: str
        """
        return self.configparser['TestSettings'][settingName].strip("'")

    def __createTarget(self):
        db = Database(host=self.host)
        db.DatabaseName = self.databaseName
        db.Verbose = True
        return db


if __name__ == '__main__':
    unittest.main()
