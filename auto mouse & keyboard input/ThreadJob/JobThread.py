import threading
import pyautogui
from ThreadJob.JobManager import JobManager

class JobThread(threading.Thread):
    name = "lineChunkThread"
    jobManager:JobManager=None

    def __init__(self, jm:JobManager):
        threading.Thread.__init__(self)
        self.jobManager = jm

    def run(self):
        for i in range(len(self.jobManager.getTaskList())):
            self.jobManager.start(i)


