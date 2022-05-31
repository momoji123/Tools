from time import sleep

class TaskManager:

    tasks=[]
    delay=0.1

    def __init__(self):
        pass

    def addTask(self, task):
        self.tasks.append(task)
        return self

    def setTasks(self, tasks):
        self.tasks = tasks

    def removeTask(self, taskId):
        for i in range(len(self.tasks)):
            if self.tasks[i].id == taskId:
                self.tasks.pop(i)
        return self

    def startAllTasks(self):
        for task in self.tasks:
            task.start()
            sleep(self.delay)
