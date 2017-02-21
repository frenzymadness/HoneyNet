import threading
from random import choice


class HTTP(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.c = config

    def run(self):
        print("starting on page {}".format(self.c['start-page']))

