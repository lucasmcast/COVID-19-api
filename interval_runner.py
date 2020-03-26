from threading import Thread
from time import sleep

class IntervalRunner(Thread):
    
    def __init__(self, interval, function):
        Thread.__init__(self)

        self.interval = interval
        self.function = function
        self.executing = False

    def run(self):
        self.executing = True
        while self.executing:
            self.function()
            sleep(self.interval)
    
    def stop(self):
        self.executing = False
