from Util.TaskManager import TaskManager


class JobManager:

    taskManagers = None

    def __init__(self):
        self.taskManagers = []

    def registerTask(self, task:TaskManager):
        self.taskManagers.append(task)

    def removeTask(self, index):
        self.taskManagers.pop(index)

    def getTaskList(self):
        return self.taskManagers

    def startAll(self):
        for tm in self.taskManagers:
            tm.startAllTasks()
            tm.setTasks([])

    def start(self, index):
        self.taskManagers[index].startAllTasks()
        self.taskManagers[index].setTasks([])
