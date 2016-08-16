import mysql.connector
import datetime
import random


class Database:
    def __init__(self, host='127.0.0.1'):
        self.connector = None
        self.Verbose = False
        self.DatabaseName = "HUMIDITY"
        self.TableName = "humidity"
        self.user = "client"
        self.password = "client"
        self.host = host

    def create(self, adminUser='root', adminPassword='', recreate=False):
        if self.checkDatabaseExist(adminUser, adminPassword):
            self.__log("database exist")
            if recreate:
                self.connector.cmd_query("DROP DATABASE {};".format(self.DatabaseName))
        else:
            self.__createDatabase()

            if not self.__checkUserExist():
                table = self.DatabaseName + '.' + self.TableName
                self.__createAndGrant("'{}'@'localhost'".format(self.user), table)
                self.__createAndGrant("'{}'@'%'".format(self.user), table)

    def drop(self, adminUser='root', adminPassword=''):
        if self.checkDatabaseExist(adminUser, adminPassword):
            self.connector.cmd_query("DROP DATABASE {};".format(self.DatabaseName))

    def writeValue(self, value, time=None):
        self.__createUsersConnector()

        if time is None:
            time = datetime.datetime.now()

        cur = self.connector.cursor()
        cur.execute("INSERT INTO {database}.{table}(date,value) VALUES(%s, %s)"
                    .format(database=self.DatabaseName, table=self.TableName),
                    (time.strftime("%Y-%m-%d %H:%M:%S"), value))
        self.connector.commit()
        self.__closeConnector()

    def getValues(self, start, stop):
        self.__createUsersConnector()
        cur = self.connector.cursor()
        cur.execute("SELECT date,value FROM {database}.{table} WHERE date>=%s and date<=%s ORDER BY date".
                    format(database=self.DatabaseName,
                           table=self.TableName),
                    (start.strftime("%Y-%m-%d %H:%M:%S"), stop.strftime("%Y-%m-%d %H:%M:%S")))
        return cur.fetchall()

    def checkDatabaseExist(self, adminUser, adminPassword):
        self.__createConnector(adminUser, adminPassword)
        cur = self.connector.cursor()
        cur.execute("SHOW DATABASES;")
        rows = cur.fetchall()
        return self.DatabaseName in (r[0] for r in rows)

    def _connectorFabric(self, user, password):
        return mysql.connector.Connect(host=self.host, user=user, password=password)

    def __checkUserExist(self):
        cur = self.connector.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{}')".format(self.user))
        rows = cur.fetchall()
        return rows[0][0] == 1

    def __createUsersConnector(self):
        self.__closeConnector()
        self.__createConnector(self.user, self.password)
        self.connector.database = self.DatabaseName

    def __createConnector(self, user, password):
        if self.connector is None:
            self.connector = self._connectorFabric(user, password)
            self.connector.connect()

    def __createDatabase(self):
        self.__log("creating database")
        query = """CREATE DATABASE {database};
USE {database};
CREATE TABLE {table}(id int auto_increment primary key, date datetime, value double, index timeindex(date));
""".format(database=self.DatabaseName, table=self.TableName)
        self.__executeBatch(query)

    def __createAndGrant(self, username, tablename):
        self.__log("creating user " + username)
        query = """
        CREATE USER {user} IDENTIFIED BY '{password}';
        GRANT ALL PRIVILEGES ON {tablename} TO {user};
        """.format(user=username, password=self.password, tablename=tablename)
        self.__executeBatch(query)

    def __executeBatch(self, query):
        self.__log(query)
        it = self.connector.cmd_query_iter(query)
        if it is not None:
            for i in it:
                self.__log(i)

    def __closeConnector(self):
        if self.connector is None:
            return
        self.connector.close()
        self.connector = None

    def __log(self, message):
        if self.Verbose:
            print(message)
