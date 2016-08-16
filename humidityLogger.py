import threading


class HumidityLogger:
    def __init__(self, interval, log_func):
        self.__t = threading.Thread(target=self.__main)
        self.__stop = threading.Event()
        self.__interval = interval
        self.__log = log_func
        self.running = False

    def start(self):
        if self.running:
            return
        self.__t.start()
        self.running = True

    def stop(self):
        if not self.running:
            return
        self.__stop.set()
        self.__t.join()
        self.running = False

    def __main(self):
        while not self.__stop.wait(self.__interval):
            self.__log()


if __name__ == '__main__':
    import time

    h = HumidityLogger(3, lambda: print('ok'))
    h.start()

    while input() != 'q':
        print(time.time())

    h.stop()
    print('done')
