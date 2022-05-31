import pyautogui
from Util.TaskBuilder import TaskBuilder, TaskMode
from Util.MouseTask import MouseBtn, TaskTyp
from Util.KeyboardTask import TaskType
import Util.TaskFactory as tf
from Util.TaskManager import TaskManager
from ThreadJob.JobManager import JobManager
from ThreadJob.JobThread import JobThread
import keyboard
import sys


def main():
    pyautogui.FAILSAFE = False
    tm = TaskManager()
    jobManager = JobManager()

    ### START JOB ###

    # open browser
    tm.addTask(tf.doLeftSingleClick(768, 1053))
    registerTask(tm, jobManager)

    # open explorer
    tm.addTask(tf.doLeftSingleClick(647, 1062))
    tm.addTask(tf.doLeftSingleClick(506, 942))
    registerTask(tm, jobManager)

    nameList = getNameList()
    classList = getClassList()
    for i in range(len(nameList)):
        # move mouse to first foto
        tm.addTask(tf.doMoveMouse(291, 387))
        # drag to upload
        tm.addTask(tf.doDragMouse(912, 561))
        # wait until upload finish
        tm.addTask(tf.doWait(3))
        registerTask(tm, jobManager)

        # click foto
        tm.addTask((tf.doLeftSingleClick(694, 569)))
        # move mouse to photo in canvas
        tm.addTask(tf.doMoveMouse(1417, 559))
        # drag to frame
        tm.addTask(tf.doDragMouse(1402, 560))
        registerTask(tm, jobManager)

        # click name
        tm.addTask(tf.doLeftDoubleClick(1655, 554))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        # type name
        tm.addTask(tf.doKeyboardTyping(nameList[i]))
        tm.addTask(tf.doKeyboardPress(["enter"]))
        # type class
        tm.addTask(tf.doKeyboardTyping(classList[i]))
        registerTask(tm, jobManager)

        # TODO: save
        # click share btn
        tm.addTask(tf.doLeftSingleClick(1857, 171))
        # click download btn
        tm.addTask(tf.doLeftSingleClick(1618, 785))
        # wait
        tm.addTask(tf.doWait(3))
        # download
        tm.addTask(tf.doLeftSingleClick(1679, 686))
        # wait
        tm.addTask(tf.doWait(18))
        registerTask(tm, jobManager)

        # click option
        tm.addTask(tf.doLeftSingleClick(722, 505))
        tm.addTask(tf.doWait(0.5))
        # click delete
        tm.addTask(tf.doLeftSingleClick(941, 810))
        tm.addTask(tf.doWait(0.4))
        registerTask(tm, jobManager)

        # reset selection
        tm.addTask(tf.doLeftSingleClick(1197, 293))
        # click frame
        tm.addTask(tf.doLeftSingleClick(1320, 564))
        # delete
        tm.addTask(tf.doKeyboardPress(["delete"]))
        registerTask(tm, jobManager)

        # move mouse to first foto in explorer
        tm.addTask(tf.doLeftSingleClick(291, 387))
        # delete photo in explorer
        tm.addTask(tf.doKeyboardCombination(["shift", "delete"]))
        tm.addTask(tf.doWait(0.3))
        registerTask(tm, jobManager)

        tm.addTask(tf.doKeyboardPress(["enter"]))
        tm.addTask(tf.doWait(0.3))
        registerTask(tm, jobManager)

    ### END OF JOB ###

    runningThread = start(jobManager)
    while runningThread.is_alive():
        if keyboard.is_pressed("esc") is True and  keyboard.is_pressed("ctrl"):
            sys.exit(1)


def registerTask(tm, jm:JobManager):
    jm.registerTask(tm)


def start(jobManager:JobManager):
    runningThread = JobThread(jobManager)
    runningThread.setDaemon(True)
    runningThread.start()
    return runningThread


# helper method for particular job
def getNameList():
    file = openFile()
    lines = file.readlines()
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[0].replace("\n", ""))
    file.close()
    return result


def getClassList():
    file = openFile()
    lines = file.readlines();
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[1].replace("\n", ""))
    file.close()
    return result


def openFile():
    return open("XII MIPA 5 DATA NAMA.csv", "r")


if __name__=="__main__":
    main()
