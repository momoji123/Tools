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
    nameList = getNameList()
    classList = getClassList()

    #openBrowser
    tm.addTask(tf.doLeftSingleClick(346,1061))

    #open explorer
    tm.addTask(tf.doLeftSingleClick(168,1061))
    tm.addTask(tf.doLeftSingleClick(52,948))

    for i in range(len(nameList)):
        # reset point
        resetPoint(tm)

        #insert name
        tm.addTask(tf.doLeftDoubleClick(2902,494))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        tm.addTask(tf.doKeyboardTyping(nameList[i]))

        #reset point
        resetPoint(tm)

        #insert class
        tm.addTask(tf.doLeftDoubleClick(2901,574))
        tm.addTask(tf.doKeyboardCombination(["ctrl", "a"]))
        tm.addTask(tf.doKeyboardTyping(classList[i]))

        # reset point
        resetPoint(tm)

        #move to photo
        tm.addTask(tf.doMoveMouse(1751,279))
        #drag
        tm.addTask(tf.doDragMouse(2070,386))
        tm.addTask(tf.doWait(2))
        #click photo to insert
        tm.addTask(tf.doLeftSingleClick(2058,411))

        # reset point
        resetPoint(tm)

        #move to photo
        tm.addTask(tf.doMoveMouse(2828,374))
        #drag to frame
        tm.addTask(tf.doDragMouse(2802,382))

        # reset point
        resetPoint(tm)

        #share
        tm.addTask(tf.doLeftSingleClick(3406,94))
        #download btn
        tm.addTask(tf.doLeftSingleClick(3232,580))
        #click dropdown
        tm.addTask(tf.doLeftSingleClick(3245,234))
        #click type
        tm.addTask(tf.doLeftSingleClick(3162,462))
        tm.addTask(tf.doWait(1))
        #donwload
        tm.addTask(tf.doLeftSingleClick(3254,346))
        tm.addTask(tf.doWait(25))

        #click option
        tm.addTask(tf.doLeftSingleClick(2078,365))
        tm.addTask(tf.doWait(0.5))
        #delete
        tm.addTask(tf.doLeftSingleClick(2194,618))
        #click frame
        tm.addTask(tf.doLeftSingleClick(2901,386))
        #delete
        tm.addTask(tf.doKeyboardPress(["delete"]))
        #click photo
        tm.addTask(tf.doLeftSingleClick(1744,263))
        tm.addTask(tf.doKeyboardCombination(["shift", "delete"]))
        tm.addTask(tf.doWait(0.5))
        tm.addTask(tf.doKeyboardPress(["enter"]))
        tm.addTask(tf.doWait(1))

    ### END OF JOB ###

    jobManager.registerTask(tm)
    runningThread = start(jobManager)
    while runningThread.is_alive():
        if keyboard.is_pressed("esc") is True and  keyboard.is_pressed("ctrl"):
            sys.exit(1)

def resetPoint(tm):
    tm.addTask(tf.doLeftSingleClick(2480,221))

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
    lines = file.readlines()
    result = []
    for l in lines:
        splitted = l.split(",")
        result.append(splitted[1].replace("\n", ""))
    file.close()
    return result


def openFile():
    return open("PRESTASI MAT SC.csv", "r")


if __name__=="__main__":
    main()
