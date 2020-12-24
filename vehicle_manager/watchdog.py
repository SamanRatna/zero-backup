from threading import Timer
# import logging

# WD_LOG_FILENAME = "watchdog.log"
# WD_LOG_FORMAT = ('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# self.wdLogger=logging.getLogger("event_logger")
# self.wdLogger.setLevel(logging.INFO)
# self.wdLogger = Watchdog(30, self.watchdogHandler)
# #Handle FileNotFound error
# self.wdHandler = logging.FileHandler('../logs/watchdog.log')
# self.wdHandler.setLevel(logging.INFO)
# self.wdHandler.setFormatter(logging.Formatter(WD_LOG_FORMAT))
# self.wdLogger.addHandler(self.wdHandler)
class Watchdog(Exception):
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self