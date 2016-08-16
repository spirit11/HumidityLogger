import threading
import time
import datetime
from http.server import HTTPServer, CGIHTTPRequestHandler
import Database
import humidityLogger

import sys

sys.path.append('cgi-bin')

import DatabaseConfig

v = 1


class MyServerHandler(CGIHTTPRequestHandler):
    def __init__(self, request, client_addr, server):
        super().__init__(request, client_addr, server)

    def do_GET(self):
        self.cgi_directories = ['/cgi-bin']
        questPos = self.path.find('?')
        path = '/cgi-bin/hello.py'
        if questPos > 0:
            path += self.path[questPos::]
        self.path = path
        super().do_GET()


def logHumidity():
    global v
    DatabaseConfig.db.writeValue(v)
    v += 1


srvrobj = HTTPServer(('', 88), MyServerHandler)
logger = humidityLogger.HumidityLogger(5, logHumidity)
logger.start()

srvrThread = threading.Thread(target=srvrobj.serve_forever)
srvrThread.start()

while input() != 'q':
    print(time.time())

srvrobj.shutdown()
srvrThread.join()
logger.stop()
