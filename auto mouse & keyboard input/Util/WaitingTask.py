from time import sleep


class WaitingTask:
    duration = None

    def __init__(self):
        self.duration = 0.5

    def setDuration(self, second):
        self.duration = second
        return self

    def start(self):
        sleep(self.duration)
